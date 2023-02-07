import numpy as np
import pandas as pd
import json

with open("jsons/initial_routes.json", "r") as f:
    initial_routes = json.load(f)

df = pd.read_csv("data/info_lat_long.csv")

for vehicle_id in initial_routes:
    print(vehicle_id, initial_routes[vehicle_id])

for row in df.iterrows():
    print(row[0] + 1, (row[1]['lat'], row[1]['long']))

