import geopy.distance
import numpy as np

coord = (12.9716, 77.5946)

N = 1000
data = np.random.normal(size=(N, 2), scale=0.05, loc=coord)
data[0] = coord

dmat = np.zeros((N, N))

for i in range(N):
    for j in range(N):
        dmat[i, j] = geopy.distance.geodesic(data[i], data[j]).m
    if i % 100 == 0:
        print(i)

# print(df)
dmat = dmat.astype(int)
with open("data/distance_matrix_2000.npy", "wb") as f:
    np.save(f, dmat)
