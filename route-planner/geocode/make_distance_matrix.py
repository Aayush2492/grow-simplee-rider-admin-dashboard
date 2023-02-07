import geopy.distance
import numpy as np
import pandas as pd

coord = (12.9716, 77.5946)
lat_long = pd.read_csv('../src/data/info_lat_long.csv')

N = lat_long.shape[0]

dmat = np.zeros((N, N))

for i in range(N):
    for j in range(N):
        dmat[i, j] = geopy.distance.geodesic((lat_long['lat'][i], lat_long['long'][i]),
                                             (lat_long['lat'][j], lat_long['long'][j])).m

dmat = dmat.astype(int)
with open("../src/data/distance_matrix_sample.npy", "wb") as f:
    np.save(f, dmat)
