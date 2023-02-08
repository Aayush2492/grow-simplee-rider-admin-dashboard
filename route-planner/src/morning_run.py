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

MAX_VOLUME = [20 * 16 * 16, 20 * 12 * 12]    # 100 * 80 * 80, 100 * 60 * 60
MAX_OBJECT_SIZE = 8 * 8 * 4                  # 40 * 40 * 20
MAX_TRAVEL_TIME = 5 * 60 * 60                # 5 hours

del_df = pd.read_csv(PATH_TO_DELIVERY_DATA)
pic_df = pd.read_csv(PATH_TO_PICKUP_DATA)
today = datetime.today().date()

start_time = datetime.now()
end_time = datetime.now() + timedelta(hours=5)

number_deliveries = 150
# number_deliveries = del_df.shape[0] - 1
number_vehicles = number_deliveries // 22
# speed_factor = 6.5 # 6.5 m/s = 23.25 km/h
hub_coord = del_df["lon"][0], del_df["lat"][0]

routes = dict()


# Cluster Here and give a list of indexes of jobs
# For now, we just assume that all jobs are in one cluster
delivery_clusters = [{"vehicles": [i for i in range(1, number_vehicles + 1)],
                      "deliveries": [i for i in range(1, number_deliveries + 1)]}]

# -1 for unassigned
# -2 for delivered
# i if assigned to vehicle i
assigned_vehicle = np.array([-1 for _ in range(5000)])

for cluster in delivery_clusters:
    # Create sample_input
    inp = dict()
    inp["vehicles"] = list()
    inp["jobs"] = list()

    # Create vehicles
    for i in cluster["vehicles"]:
        inp["vehicles"].append({
            "id": i,
            "start": hub_coord,
            "end": hub_coord,
            "max_travel_time": int((end_time - datetime.now()).total_seconds()),
            "capacity": [MAX_VOLUME[i % 2] - MAX_OBJECT_SIZE - MAX_OBJECT_SIZE],
        })

    # Create jobs
    for i in cluster["deliveries"]:
        edd = datetime.strptime(del_df["edd"][i], "%Y-%m-%d").date()
        inp["jobs"].append({
            "id": i,
            "location": [float(del_df["lon"][i]), float(del_df["lat"][i])],
            "delivery": [int(del_df["volume"][i] / 125)],
            "priority": 15 if edd < today else 30 if edd == today else max(2, 10 - (edd - today).days),
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
