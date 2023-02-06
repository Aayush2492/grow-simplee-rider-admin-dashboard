import json
import subprocess

# Build vroom in this directory otherwise change the path below
PATH_TO_VROOM_EXECUTABLE = "./vroom"
PATH_TO_DISTANCE_MATRIX_FILE = "jsons/distance_matrix.json"
PATH_TO_INITIAL_ROUTES_FILE = "jsons/initial_routes.json"
PATH_TO_INPUT_FILE = "jsons/inp.json"
PATH_TO_OUTPUT_FILE = "jsons/out.json"

NUM_VEHICLES = 20
NUM_JOBS = 170
MAX_VOLUME = 30
MAX_HEIGHT = 30

# Some states
# ignored_jobs = [25, 65, 71, 91]
ignored_jobs = []
read_initial_routes = False
write_initial_routes = False


def dm_slice(arr):
    """
    Slice the distance matrix to only include the jobs we want to route
    :param arr: list of job ids
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
        "max_travel_time": 100000,  # units in matrix
        # "capacity": [MAX_VOLUME, MAX_HEIGHT],
        # "capcity": [MAX_HEIGHT],
        "max_tasks": MAX_VOLUME,
    }
    inp["vehicles"].append(x)

for i in range(NUM_JOBS):
    if i + 1 in ignored_jobs:
        continue
    x = {
        "id": i + 1001,
        "location_index": i + 1,
        # "delivery": [1, 1]  # volume, height
        # "delivery": [1]  # height
    }
    inp["jobs"].append(x)


# open file distance_matrix.json and read the data
with open(PATH_TO_DISTANCE_MATRIX_FILE, "r") as f:
    distance_matrix = json.load(f)
    inp["matrices"] = dm_slice([i for i in range(NUM_JOBS + 1)])
    inp["matrices"]["car"]["costs"] = inp["matrices"]["car"]["durations"]


# Read initial routes from file if required
if read_initial_routes:
    with open(PATH_TO_INITIAL_ROUTES_FILE, "r") as f:
        try:
            initial_routes = json.load(f)
            for vehicle_id in initial_routes:
                inp["vehicles"][int(vehicle_id) - 1]["initial_route"] = initial_routes[vehicle_id]
        except json.decoder.JSONDecodeError as e:
            print("Not processing initial routes")
    initial_routes = dict()


# Write input to file
with open(PATH_TO_INPUT_FILE, "w") as f:
    json.dump(inp, f, indent=2)


# Running vroom
subprocess.run([PATH_TO_VROOM_EXECUTABLE, "-i", PATH_TO_INPUT_FILE, "-o", PATH_TO_OUTPUT_FILE, "-l", "5"])


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
