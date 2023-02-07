import json
import subprocess
import numpy as np
import time

start_time = time.time()

# Build vroom in this directory otherwise change the path below
PATH_TO_VROOM_EXECUTABLE = "./vroom"
PATH_TO_DISTANCE_MATRIX_FILE = "data/distance_matrix.npy"
PATH_TO_INITIAL_ROUTES_FILE = "jsons/initial_routes.json"
PATH_TO_INPUT_FILE = "jsons/inp.json"
PATH_TO_OUTPUT_FILE = "jsons/out.json"

"""
We assume all the objects are of a valid size and l >= b >= h
We scale down all objects of size l x b x h to (l/5) x (b/5) x (h/5) and then 
ceiled it to the nearest power of 2.
"""

NUM_JOBS = 190
NUM_VEHICLES = NUM_JOBS // 25
NUM_VEHICLE_TYPE = [NUM_JOBS // 2, NUM_JOBS // 2]
MAX_VOLUME = [20 * 16 * 16, 20 * 12 * 12]  # 100 * 80 * 80, 100 * 60 * 60
MAX_OBJECT_SIZE = 8 * 8 * 4  # 40 * 40 * 20
SPEED_MS = 6.5  # 6.5 m/s = 23.25 km/h
MAX_TRAVEL_TIME_SEC = 5 * 60 * 60  # 5 hours

# Some states
# ignored_jobs = [25, 65, 71, 91]
ignored_jobs = []
read_initial_routes = False
write_initial_routes = True


def dm_slice(arr, distance_matrix):
    """
    Slice the distance matrix to only include the jobs we want to route
    :param arr: list of job ids
    :param distance_matrix: distance matrix
    """
    ret = dict()
    for veh in distance_matrix["matrices"]:
        ret[veh] = dict()
        for mt in distance_matrix["matrices"][veh]:
            ret[veh][mt] = [[distance_matrix["matrices"][veh][mt][_r][_c] for _c in arr] for _r in arr]
    return ret


# Create input
inp = dict()
inp["vehicles"] = list()
inp["jobs"] = list()
initial_routes = dict()

for i in range(NUM_VEHICLES):
    x = {
        "id": i + 1,
        "start_index": 0,
        "end_index": 0,
        "max_travel_time": MAX_TRAVEL_TIME_SEC,
        # "capacity": [MAX_VOLUME, MAX_HEIGHT],
        # "max_tasks": 10,
        "capcity": [MAX_VOLUME[i % 2]],
    }
    inp["vehicles"].append(x)

for i in range(NUM_JOBS):
    if i + 1 in ignored_jobs:
        continue
    x = {
        "id": i + 1001,
        "location_index": i + 1,
        # "delivery": [1, 1]  # volume, height
        "delivery": [1]  # height
    }
    inp["jobs"].append(x)

# Read the distance matrix
with open(PATH_TO_DISTANCE_MATRIX_FILE, "rb") as f:
    dm = np.load(f)
    inp["matrices"] = {"car": {"durations": (dm.astype(float) / SPEED_MS).astype(int).tolist()}}
    # inp["matrices"]["car"]["costs"] = dm

print("Time taken after reading distance matrix: ", time.time() - start_time)


# Read initial routes from file if required
if read_initial_routes:
    with open(PATH_TO_INITIAL_ROUTES_FILE, "r") as f:
        try:
            initial_routes = json.load(f)
            for vehicle_id in initial_routes:
                inp["vehicles"][int(vehicle_id) - 1]["steps"] = initial_routes[vehicle_id]
        except json.decoder.JSONDecodeError as e:
            print(e, "Not processing initial routes")
        except Exception as e:
            print(e, "Not processing initial routes")
    initial_routes = dict()


# Write input to file
with open(PATH_TO_INPUT_FILE, "w") as f:
    json.dump(inp, f)


print("Time taken after writing input file: ", time.time() - start_time)


# Running vroom
# subprocess.run([PATH_TO_VROOM_EXECUTABLE, "-i", PATH_TO_INPUT_FILE, "-o", PATH_TO_OUTPUT_FILE, "-l", "5"])
subprocess.run([PATH_TO_VROOM_EXECUTABLE, "-i", PATH_TO_INPUT_FILE, "-o", PATH_TO_OUTPUT_FILE])


print("Time taken after running vroom: ", time.time() - start_time)


# Open output file and read the data
with open(PATH_TO_OUTPUT_FILE, "r") as f:
    out = json.load(f)
    for route in out["routes"]:
        vehicle_id = route["vehicle"]
        initial_routes[vehicle_id] = list()
        for step in route["steps"]:
            if step["type"] == "start" or step["type"] == "end":
                initial_routes[vehicle_id].append({"type": step["type"]})
            else:
                initial_routes[vehicle_id].append({"type": "job", "id": step["job"]})


# Write initial routes to file
if write_initial_routes:
    with open(PATH_TO_INITIAL_ROUTES_FILE, "w") as f:
        json.dump(initial_routes, f, indent=2)


# Write output to file with pretty print
with open(PATH_TO_OUTPUT_FILE, "w") as f:
    json.dump(out, f, indent=2)


print("Time taken after writing output file: ", time.time() - start_time)
