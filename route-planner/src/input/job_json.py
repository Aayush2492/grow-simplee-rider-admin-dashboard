import json
from dm import dm, dt

NUM_VEHICLES = 50
NUM_JOBS = 190

inp = dict()
inp["vehicles"] = list()
inp["jobs"] = list()


for i in range(NUM_VEHICLES):
    x = {
        "id": i + 1,
        "max_travel_time": 5000,
        "start_index": 0,
        "end_index": 0,
        "capacity": [8]
    }
    inp["vehicles"].append(x)

for i in range(NUM_JOBS):
    x = {
        "id": i + 1001,
        "location_index": i + 1,
        "delivery": [1]
    }
    inp["jobs"].append(x)

inp["matrices"] = dict()
inp["matrices"]["car"] = dict()
inp["matrices"]["car"]["durations"] = dt
inp["matrices"]["car"]["costs"] = dm

with open("input.json", "w") as f:
    json.dump(inp, f, indent=2)
