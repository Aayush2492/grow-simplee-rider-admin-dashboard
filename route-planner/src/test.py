import numpy as np

with open("data/distance_matrix_2000.npy", "rb") as f:
    dmat = np.load(f).tolist()

print(dmat)
