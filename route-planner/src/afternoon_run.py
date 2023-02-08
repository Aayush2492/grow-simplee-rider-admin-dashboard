import numpy as np
import pandas as pd
import json
import subprocess
from datetime import datetime, timedelta

PATH_TO_VROOM_EXECUTABLE = "./vroom"
PATH_TO_FOLDER = "small_sample"
PATH_TO_DELIVERY_DATA = f"{PATH_TO_FOLDER}/deliveries.csv"
PATH_TO_PICKUP_DATA = f"{PATH_TO_FOLDER}/pickups.csv"

PATH_TO_INPUT_FILE = f"{PATH_TO_FOLDER}/temp/inp.json"
PATH_TO_OUTPUT_FILE = f"{PATH_TO_FOLDER}/temp/out.json"
PATH_TO_POST_MORN_DATA = f"{PATH_TO_FOLDER}/post_morn_data.json"
PATH_TO_POST_NOON_DATA = f"{PATH_TO_FOLDER}/post_noon_data.json"

MAX_VOLUME = [20 * 16 * 16, 20 * 12 * 12]  # 100 * 80 * 80, 100 * 60 * 60
MAX_OBJECT_SIZE = 8 * 8 * 4  # 40 * 40 * 20
MAX_TRAVEL_TIME = 5 * 60 * 60  # 5 hours

del_df = pd.read_csv(PATH_TO_DELIVERY_DATA)
pic_df = pd.read_csv(PATH_TO_PICKUP_DATA)
today = datetime.today().date()

with open(PATH_TO_POST_MORN_DATA, "r") as f:
    d = json.load(f)
    start_time = d["start_time"]
    package_info = d["package_info"]
    routes = d["routes"]
    edd_format = d["edd_format"]

start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S.%f")
cur_time = datetime.now()
time_diff = cur_time - start_time
end_time = start_time + timedelta(hours=5)

new_routes = dict()

# number_deliveries = 350
number_deliveries = del_df.shape[0] - 1
number_pickups = pic_df.shape[0] - 1
number_vehicles = number_deliveries // 22
# speed_factor = 6.5 # 6.5 m/s = 23.25 km/h
hub_coord = del_df["lon"][0], del_df["lat"][0]


def update_assigned_vehicle_and_add_to_jobs(_route, _vehicle_id):
    _steps = list({"type": "start"})
    for _step in _route["steps"]:
        if _step["type"] == "job":
            _id = str(_step["id"])
            if _step["arrival"] <= time_diff.total_seconds():
                package_info[_id]["assigned_vehicle"] = -2  # -2 means delivered
                package_info[_id]["done"] = False
                continue
            elif package_info[_id]["type"] == "delivery":
                package_info[_id] = _vehicle_id
                inp["jobs"].append({
                    "id": _step["id"],
                    "location": [float(del_df["lon"][_step["id"]]), float(del_df["lat"][_step["id"]])],
                    "delivery": [int(del_df["volume"][_step["id"]] / 125)],
                    "skills": [int(_vehicle_id)],  # This HAS to be done by this vehicle
                    "priority": 1000,  # This HAS to be done
                })
                _steps.append(_step)
            elif package_info[_id]["type"] == "pickup":
                # This is an undone pickup and hence can be procrastinated
                # Unassign the vehicle to this pickup to compute it together with the rest
                package_info[_id]["assigned_vehicle"] = -1  # -1 means not assigned
            _steps.append({
                "type": "job",
                "id": _step["id"],
            })
        elif _step["type"] == "end":
            _steps.append({
                "type": "end",
            })
    return _steps


# Cluster Here and give a list of indexes of jobs
# For now, we just assume that all jobs are in one cluster
pickup_clusters = {
    "1": {
        "vehicles": [i for i in range(1, number_vehicles + 1)],
        "deliveries": [i for i in range(1, number_deliveries + 1)],
        "pickups": [i for i in range(1, number_pickups + 1)]
    }
}


for cluster_no, cluster in pickup_clusters.items():
    # Create sample_input
    inp = dict()
    inp["vehicles"] = list()
    inp["jobs"] = list()

    # Create jobs for pickups
    for pickup_id in cluster["pickups"]:
        if package_info[str(pickup_id)] == -2:  # Already delivered
            continue
        inp["jobs"].append({
            "id": int(pickup_id),
            "location": [float(pic_df["lon"][pickup_id]), float(pic_df["lat"][pickup_id])],
            "pickup": [int(pic_df["volume"][pickup_id] / 125)],
            "priority": 3,
        })

    # Create vehicles
    for vehicle_id in cluster["vehicles"]:
        inp["vehicles"].append({
            "id": int(vehicle_id),
            "start": hub_coord,  # TODO change to pickup location
            "end": hub_coord,
            "max_travel_time": int((end_time - cur_time).total_seconds()),
            "capacity": [MAX_VOLUME[vehicle_id % 2] - MAX_OBJECT_SIZE],
            "skills": [vehicle_id]
        })

        if str(vehicle_id) in routes:
            steps = update_assigned_vehicle_and_add_to_jobs(routes[vehicle_id], vehicle_id)
            if len(steps) > 2:
                inp["vehicles"][-1]["steps"] = steps

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
        new_routes[vehicle_id] = list()
        for step in route["steps"]:
            new_routes[vehicle_id].append({"type": step["type"], "arrival": step["arrival"]})
            if step["type"] == "job":
                package_info[str(step["id"])]["assigned_vehicle"] = vehicle_id
                new_routes[vehicle_id][-1]["id"] = step["id"]


with open(PATH_TO_POST_NOON_DATA, "w") as f:
    d = dict()
    d["start_time"] = start_time.__str__()
    d["routes"] = new_routes
    json.dump(d, f)
