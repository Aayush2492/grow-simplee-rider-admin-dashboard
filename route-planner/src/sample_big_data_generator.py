import numpy as np
import pandas as pd
import datetime

hub_cords = (77.5942765, 12.9719418)  # Bangalore

max_bangalore_lat = 13.20
min_bangalore_lat = 12.84

max_bangalore_lon = 77.76
min_bangalore_lon = 77.35

area_cords = {
    "indiranagar": (77.640612, 12.971643),
    "marathahalli": (77.698116, 12.955210),
    "whitefield": (77.749481, 12.969120),
    "koramangala": (77.625320, 12.927880),
    "bellandur": (77.676670, 12.925170),
    "jayanagar": (77.582000, 12.929200),
    "kormangala": (77.625320, 12.927880),
    "kalyan_nagar": (77.636200, 12.990500),
    "vijayanagar": (77.536013, 12.961016),
    "kengeri": (77.481344, 12.901475),
    "hsr_layout": (77.638200, 12.916700),
}

np_arr = np.array(list(area_cords.values()))
print(np_arr)

# N = 3000
#
# data = list()
# data.append([0, 0, hub_cords[0], hub_cords[1], datetime.datetime.today().date()])
#
# done = 0
# while done < N:
#     lon, lat = np.random.normal(size=(1, 2), scale=0.05, loc=hub_cords)[0]
#     if not (min_bangalore_lon <= lon <= max_bangalore_lon):
#         continue
#     if not (min_bangalore_lat <= lat <= max_bangalore_lat):
#         continue
#     volume = 125 * (2 ** np.random.randint(0, 12))  # 125 * (1 to 2^11)
#     edd = datetime.datetime.today().date() + datetime.timedelta(days=int(np.random.choice([0, 0, 0, 1, 1, 2, 3])))
#     data.append([done+1, volume, round(lon, 8), round(lat, 8), edd])
#     done += 1
#
# df = pd.DataFrame(data=data, columns=["id", "volume", "lon", "lat", "edd"])
#
# df.to_csv("big_sample/all_points.csv", index=False)
# df[:2001].to_csv("big_sample/deliveries.csv", index=False)
# df[2001:2501].to_csv("big_sample/returns.csv", index=False)
# df[2501:].to_csv("big_sample/returns.csv", index=False)
