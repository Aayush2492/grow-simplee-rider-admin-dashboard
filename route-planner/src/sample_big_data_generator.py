import numpy as np
import pandas as pd
import datetime

hub_cords = (77.5942765, 12.9719418)  # Bangalore

max_bangalore_lat = 13.20
min_bangalore_lat = 12.84

max_bangalore_lon = 77.76
min_bangalore_lon = 77.35

N = 3000

data = list()
data.append([0, 0, hub_cords[0], hub_cords[1], datetime.datetime.today().date()])

done = 0
while done < N:
    lon, lat = np.random.normal(size=(1, 2), scale=0.05, loc=hub_cords)[0]
    if not (min_bangalore_lon <= lon <= max_bangalore_lon):
        continue
    if not (min_bangalore_lat <= lat <= max_bangalore_lat):
        continue
    volume = 125 * (2 ** np.random.randint(0, 12))  # 125 * (1 to 2^11)
    edd = datetime.datetime.today().date() + datetime.timedelta(days=int(np.random.choice([0, 0, 0, 1, 1, 2, 3])))
    data.append([done+1, volume, round(lon, 8), round(lat, 8), edd])
    done += 1

df = pd.DataFrame(data=data, columns=["id", "volume", "lon", "lat", "edd"])

df.to_csv("sample_big_input/all_points.csv", index=False)
df[:2001].to_csv("sample_big_input/deliveries.csv", index=False)
df[2001:].to_csv("sample_big_input/returns.csv", index=False)
