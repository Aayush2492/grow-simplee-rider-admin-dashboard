import pandas as pd
import json
import subprocess
import time
from datetime import datetime

start_time = time.time()

PATH_TO_VROOM_EXECUTABLE = "./vroom"
PATH_TO_DELIVERY_DATA = "big_sample/deliveries.csv"
PATH_TO_INPUT_FILE = "big_sample/temp/inp.json"
PATH_TO_OUTPUT_FILE = "big_sample/temp/out.json"
PATH_TO_MORN_ROUTES = "big_sample/morn_routes.json"

inp_df = pd.read_csv(PATH_TO_DELIVERY_DATA)

# number_jobs = inp_df.shape[0] - 1
number_jobs = 100
number_vehicles = number_jobs // 22
max_volume = [20 * 16 * 16, 20 * 12 * 12]    # 100 * 80 * 80, 100 * 60 * 60
max_object_size = 8 * 8 * 4                  # 40 * 40 * 20
max_travel_time = 5 * 60 * 60                # 5 hours
# speed_factor = 6.5                           # 6.5 m/s = 23.25 km/h
today = datetime.today().date()
hub_coord = inp_df["lon"][0], inp_df["lat"][0]

routes = dict()


# Cluster Here and give a list of indexes of jobs
# For now, we just assume that all jobs are in one cluster
clusters = [{"vehicles": [i for i in range(1, number_vehicles + 1)], "jobs": [i for i in range(1, number_jobs + 1)]}]

for cluster in clusters:
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
            "capacity": [max_volume[i % 2] - max_object_size - max_object_size],
        })

    # Create jobs
    for i in cluster["jobs"]:
        edd = datetime.strptime(inp_df["edd"][i], "%Y-%m-%d").date()
        inp["jobs"].append({
            "id": i,
            "location": [float(inp_df["lon"][i]), float(inp_df["lat"][i])],
            "delivery": [int(inp_df["volume"][i] / 125)],
            "service": 60,
            "priority": 15 if edd < today else 30 if edd == today else max(2, (edd - today).days),
        })

    # Write inp to file
    with open(PATH_TO_INPUT_FILE, "w") as f:
        json.dump(inp, f)

    # Run vroom
    subprocess.run([PATH_TO_VROOM_EXECUTABLE, "-i", PATH_TO_INPUT_FILE, "-o", PATH_TO_OUTPUT_FILE])

    # Read output
    with open(PATH_TO_OUTPUT_FILE, "r") as f:
        out = json.load(f)
