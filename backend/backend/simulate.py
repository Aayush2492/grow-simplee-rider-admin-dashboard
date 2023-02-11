import json

# This functions reads the geoJSON file and return a dictionary with vehile/driver_id as key and the coordinates as value
def simulate():
    ans = {}
    num_tours = 40
    for i in range(num_tours):
        tour_id = i + 1

        data = json.load(open(f"geo_jsons/{tour_id}_geo.json"))
        if data:
            coords = data["features"][0]["coordinates"]

            for_time = json.load(open(f"jsons/{tour_id}.json"))
            time_remaining = for_time[f"{tour_id}"][-1]["arrival"]
            new_idx = (3600 * len(coords)) // time_remaining
            if new_idx >= len(coords):
                new_idx = len(coords) - 1

            ans[tour_id] = coords[new_idx]
        else:
            print("No data for tour_id: ", tour_id)

    return ans        