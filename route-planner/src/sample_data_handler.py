import pandas as pd
import geocoder  # pip install geocoder
import geopy.distance
import numpy as np

# read xlsx
data = pd.read_excel('sample_input/bangalore dispatch address.xlsx')

df = {'prod_id': [], 'edd': [], 'lat': [], 'long': []}

# iterate over rows
for index, row in data.iterrows():
    address = row[0]
    g = geocoder.bing(address, key='Ag3_-x9aIPCQxhENQQcDUeFWirDR4tvRr1YUArJF9nrvnUnBv2wis5jue73E_Nxe')
    prod_id = row[3]
    edd = row[4]
    results = g.json
    lat, long = float(results['lat']), float(results['lng'])
    if lat < 12.86 or lat > 13.22 or long < 77.32 or long > 77.90:
        continue
    df['prod_id'].append(prod_id)
    df['edd'].append(edd)
    df['lat'].append(results['lat'])
    df['long'].append(results['lng'])
    print(results['lat'], results['lng'])

df = pd.DataFrame(df)

# Convert to csv file
df.to_csv('data/info_lat_long.csv', index=False)

coord = (12.9716, 77.5946)
N = df.shape[0]

dmat = np.zeros((N+1, N+1))

for i in range(N):
    for j in range(N):
        dmat[i + 1, j + 1] = geopy.distance.geodesic((df['lat'][i], df['long'][i]),
                                                     (df['lat'][j], df['long'][j])).m

for i in range(N):
    dmat[i + 1, 0] = geopy.distance.geodesic((df['lat'][i], df['long'][i]), coord).m
    dmat[0, i + 1] = geopy.distance.geodesic(coord, (df['lat'][i], df['long'][i])).m

dmat = dmat.astype(int)
with open("data/distance_matrix_sample.npy", "wb") as f:
    np.save(f, dmat)
