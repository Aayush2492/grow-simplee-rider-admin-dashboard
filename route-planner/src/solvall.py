import numpy as np
import pandas as pd
import json
import subprocess
from datetime import datetime, timedelta

PATH_TO_VROOM_EXECUTABLE = "./vroom"
PATH_TO_FOLDER = "small_sample"
_PATH_TO_DELIVERY_DATA = f"{PATH_TO_FOLDER}/deliveries_0.csv"
_PATH_TO_PICKUP_DATA = f"{PATH_TO_FOLDER}/pickups_0.csv"
# _PATH_TO_PICKUP_DATA = None

PATH_TO_INPUT_FILE = f"{PATH_TO_FOLDER}/temp/morn_inp.json"
PATH_TO_OUTPUT_FILE = f"{PATH_TO_FOLDER}/temp/morn_out.json"
_PATH_TO_POST_MORN_DATA = f"{PATH_TO_FOLDER}/post_morn_data.json"

# MAX_OBJECT_SIZE = 8 * 8 * 4  # 40 * 40 * 20
MAX_OBJECT_SIZE = 1
# MAX_VOLUME = [20 * 16 * 16, 20 * 12 * 12 - 2]
# MAX_VOLUME = [20 * MAX_OBJECT_SIZE, 9 * MAX_OBJECT_SIZE]
MAX_VOLUME = [32 * MAX_OBJECT_SIZE, 32 * MAX_OBJECT_SIZE]
MAX_TRAVEL_TIME = 5 * 60 * 60  # 5 hours
SPEED_FACTOR = 0.8  # 6.5 m/s = 23.25 km/h


def solver(vehicles_list, cur_time=datetime.now(), is_morning=True,
           PATH_TO_DELIVERY_DATA=_PATH_TO_DELIVERY_DATA,
           PATH_TO_PICKUP_DATA=_PATH_TO_PICKUP_DATA,
           PATH_TO_OUT_FILE=_PATH_TO_POST_MORN_DATA):
    cur_time -= timedelta(days=4)
    del_df = pd.read_csv(PATH_TO_DELIVERY_DATA)
    pic_df = pd.DataFrame(columns=["id", "volume", "lon", "lat"])
    if PATH_TO_PICKUP_DATA is not None:
        pic_df = pd.read_csv(PATH_TO_PICKUP_DATA)
    today = cur_time.date()

    start_time = datetime.now()

    # number_deliveries = 150
    # number_deliveries = del_df.shape[0] - 1
    # number_pickups = pic_df.shape[0]
    # number_vehicles = number_deliveries // 22
    hub_coord = del_df["lat"][0], del_df["lon"][0]
    edd_format = "%d-%m-%Y"

    routes = dict()

    package_info = dict()
    vehicle_info = dict()

    vehicle_ids = list()
    delivery_ids = list()
    pickup_ids = list()

    for vehicle in vehicles_list:
        _id = str(vehicle["id"])
        vehicle_ids.append(_id)
        vehicle_info[_id] = vehicle

    for idx, row in del_df.iterrows():
        if idx == 0:
            continue
        delivery_id = str(del_df["id"][idx])
        delivery_ids.append(delivery_id)
        package_info[delivery_id] = {
            "type": "delivery",
            "done": False,
            "assigned_vehicle": -1,
            "location": [float(del_df["lat"][idx]), float(del_df["lon"][idx])],
            # "volume": int(del_df["volume"][idx]) // 125,
            "volume": 1,
            "edd": del_df["edd"][idx],
        }

    for idx, row in pic_df.iterrows():
        pickup_id = str(idx + 5000)
        pickup_ids.append(pickup_id)
        package_info[pickup_id] = {
            "type": "pickup",
            "done": False,
            "assigned_vehicle": -1,
            "location": [float(pic_df["lon"][idx]), float(pic_df["lat"][idx])],
            # "volume": int(pic_df["volume"][idx]) // 125,
            "volume": 1,
        }

    # Cluster Here and give a list of indexes of jobs
    # For now, we just assume that all jobs are in one cluster

    # from cluster import cluster_all
    # delivery_clusters = cluster_all(vehicle_ids, is_morning,
    #                                 PATH_TO_DELIVERY_DATA,
    #                                 PATH_TO_PICKUP_DATA)

    delivery_clusters = {
        "1": {
            "vehicles": vehicle_ids,
            "deliveries": delivery_ids,
            "pickups": pickup_ids
        }
    }

    for cluster_no, cluster in delivery_clusters.items():
        # Create sample_input
        inp = dict()
        inp["vehicles"] = list()
        inp["jobs"] = list()

        # Create vehicles
        for vehicle_id in cluster["vehicles"]:
            inp["vehicles"].append({
                "id": int(vehicle_id),
                "start": hub_coord,
                "end": hub_coord,
                "skills": [int(vehicle_id)],
                "max_travel_time": vehicle_info[vehicle_id]["time_left"],
                "capacity": [MAX_VOLUME[int(vehicle_id) % 2] - MAX_OBJECT_SIZE],
            })

            if vehicle_info[vehicle_id]["steps"]:
                inp["vehicles"][-1]["start"] = vehicle_info[vehicle_id]["location"]
                inp["vehicles"][-1]["capacity"]: [MAX_VOLUME[int(vehicle_id) % 2]]
                inp["vehicles"][-1]["steps"] = [{"type": "start"}]
                for step in vehicle_info[vehicle_id]["steps"][:-1]:
                    package_info[str(step)]["assigned_vehicle"] = int(vehicle_id)
                    inp["vehicles"][-1]["steps"].append({
                        "type": package_info[str(step)]["type"],
                        "id": package_info[str(step)]["id"],
                    })
                inp["vehicles"][-1]["steps"].append({"type": "end"})

        # Create jobs
        for delivery_id in cluster["deliveries"]:
            edd = datetime.strptime(package_info[delivery_id]["edd"], edd_format).date()
            inp["jobs"].append({
                "id": int(delivery_id),
                "location": package_info[delivery_id]["location"],
                "delivery": [package_info[delivery_id]["volume"]],
                "priority": 20 if edd < today else 40 if edd == today else max(2, 15 - (edd - today).days),
            })
            if package_info[delivery_id]["assigned_vehicle"] != -1:
                inp["jobs"][-1]["skills"] = [package_info[delivery_id]["assigned_vehicle"]]
                inp["jobs"][-1]["priority"] = 5000

        for pickup_id in cluster["pickups"]:
            inp["jobs"].append({
                "id": int(pickup_id),
                "location": package_info[pickup_id]["location"],
                "pickup": [package_info[pickup_id]["volume"]],
                # "pickup": [1],
                "priority": 10,
            })

        # Write inp to file
        with open(PATH_TO_INPUT_FILE, "w") as f:
            json.dump(inp, f)

        # Run vroom
        subprocess.run([PATH_TO_VROOM_EXECUTABLE, "-i", PATH_TO_INPUT_FILE, "-o", PATH_TO_OUTPUT_FILE, "-g"])

        # Read output
        with open(PATH_TO_OUTPUT_FILE, "r") as f:
            out = json.load(f)

        # Save to routes and update assigned_vehicle
        for route in out["routes"]:
            vehicle_id = str(route["vehicle"])
            routes[vehicle_id] = list()
            for step in route["steps"]:
                routes[vehicle_id].append({"type": step["type"], "arrival": step["arrival"]})
                if step["type"] == "job":
                    package_info[str(step["id"])]["assigned_vehicle"] = vehicle_id
                    routes[vehicle_id][-1]["id"] = step["job"]

    with open(PATH_TO_OUT_FILE, "w") as f:
        d = dict()
        d["start_time"] = start_time.__str__()
        d["edd_format"] = edd_format
        d["package_info"] = package_info
        d["routes"] = routes
        json.dump(d, f)


if __name__ == "__main__":
    VEHICLES = [
        {"id": str(1 + i), "steps": [], "time_left": MAX_TRAVEL_TIME}
        for i in range(45)
    ]
    solver(VEHICLES, cur_time=datetime.now())
