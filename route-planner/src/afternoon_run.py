import numpy as np
import pandas as pd
import json
import subprocess
from datetime import datetime
from datetime import timedelta

PATH_TO_VROOM_EXECUTABLE = "./vroom"
PATH_TO_DELIVERY_DATA = "big_sample/deliveries.csv"
PATH_TO_PICKUP_DATA = "big_sample/pickups.csv"

PATH_TO_INPUT_FILE = "big_sample/temp/inp.json"
PATH_TO_OUTPUT_FILE = "big_sample/temp/out.json"
PATH_TO_POST_MORN_DATA = "big_sample/post_morn_data.json"

MAX_VOLUME = [20 * 16 * 16, 20 * 12 * 12]  # 100 * 80 * 80, 100 * 60 * 60
MAX_OBJECT_SIZE = 8 * 8 * 4  # 40 * 40 * 20
MAX_TRAVEL_TIME = 5 * 60 * 60  # 5 hours

del_df = pd.read_csv(PATH_TO_DELIVERY_DATA)
pic_df = pd.read_csv(PATH_TO_PICKUP_DATA)
today = datetime.today().date()

with open(PATH_TO_POST_MORN_DATA, "r") as f:
    d = json.load(f)
    start_time = d["start_time"]
    cur_time = datetime.now()
    time_diff = cur_time - start_time
    end_time = start_time + timedelta(hours=5)
    assigned_vehicle = np.array(d["assigned_vehicle"])
    routes = d["routes"]


# number_deliveries = 350
number_deliveries = del_df.shape[0] - 1
number_pickups = pic_df.shape[0] - 1
number_vehicles = number_deliveries // 22
# speed_factor = 6.5 # 6.5 m/s = 23.25 km/h
hub_coord = del_df["lon"][0], del_df["lat"][0]

# Cluster Here and give a list of indexes of jobs
# For now, we just assume that all jobs are in one cluster
pickup_clusters = [{"vehicles": [i for i in range(1, number_vehicles + 1)],
                    "deliveries": [i for i in range(1, number_deliveries + 1)],
                    "pickups": [i for i in range(1, number_pickups + 1)]}]


def update_assigned_vehicle_and_add_to_jobs(_route, _vehicle_id):
    _steps = list({"type": "start"})
    for step in _route["steps"]:
        if step["type"] == "job" and step["arrival"] <= time_diff.total_seconds():
            assigned_vehicle[step["job"]] = -2  # -2 means delivered
            continue
        elif step["type"] == "job" and step["id"] <= 5000:
            # This is a delivery and HAS to be performed by the current vehicle
            inp["jobs"].append({
                "id": step["id"],
                "location": [float(del_df["lon"][step["id"]]), float(del_df["lat"][step["id"]])],
                "delivery": [int(del_df["volume"][step["id"]] / 125)],
                "skills": [int(_vehicle_id)],  # This HAS to be done by this vehicle
                "priority": 1000,  # This HAS to be done
            })
        elif step["type"] == "job" and step["id"] > 5000:
            # This is an undone pickup and hence can be procrastinated
            # Unassign the vehicle to this pickup to compute it together with the rest
            assigned_vehicle[step["id"]] = -1  # -1 means not assigned
        if step["type"] == "job":
            _steps.append({
                "type": "job",
                "id": step["id"],
            })
        elif step["type"] == "end":
            _steps.append({
                "type": "end",
            })
    return _steps


for cluster in pickup_clusters:
    # Create sample_input
    inp = dict()
    inp["vehicles"] = list()
    inp["jobs"] = list()

    # Create vehicles
    for vehicle_id in cluster["vehicles"]:
        inp["vehicles"].append({
            "id": vehicle_id,
            "start": hub_coord,  # TODO change to pickup location
            "end": hub_coord,
            "max_travel_time": int((end_time - datetime.now()).total_seconds()),
            "capacity": [MAX_VOLUME[vehicle_id % 2] - MAX_OBJECT_SIZE],
            "skills": [vehicle_id],
            "steps": update_assigned_vehicle_and_add_to_jobs(routes[vehicle_id], vehicle_id)
        })

    # Create jobs for pickups
    for pickup_id in cluster["pickups"]:
        if assigned_vehicle[int(pickup_id)] == -2:
            continue
        edd = datetime.strptime(pic_df["edd"][pickup_id], "%Y-%m-%d").date()
        inp["jobs"].append({
            "id": pickup_id,
            "location": [float(pic_df["lon"][pickup_id]), float(pic_df["lat"][pickup_id])],
            "pickup": [int(pic_df["volume"][pickup_id] / 125)],
            "priority": 3 if edd == today else 1,
        })

    # Write inp to file
    with open(PATH_TO_INPUT_FILE, "w") as f:
        json.dump(inp, f)

    # Run vroom
    subprocess.run([PATH_TO_VROOM_EXECUTABLE, "-i", PATH_TO_INPUT_FILE, "-o", PATH_TO_OUTPUT_FILE])

    # Read output
    with open(PATH_TO_OUTPUT_FILE, "r") as f:
        out = json.load(f)

    # Save to routes and update assigned_vehicle
    for route in out["routes"]:
        vehicle_id = route["vehicle"]
        routes[vehicle_id] = list()
        for step in route["steps"]:
            routes[vehicle_id].append({"type": step["type"], "arrival": step["arrival"]})
            if step["type"] == "job":
                assigned_vehicle[step["job"]] = vehicle_id
                routes[vehicle_id][-1]["id"] = step["job"]


with open(PATH_TO_POST_MORN_DATA, "w") as f:
    d = dict()
    d["start_time"] = start_time.__str__()
    d["assigned_vehicle"] = assigned_vehicle.tolist()
    d["routes"] = routes
    json.dump(d, f)
