import json
import numpy as np

with open("jsons/distance_matrix.json", "r") as f:
    distance_matrix = json.load(f)["matrices"]["car"]["durations"]
    # Convert the distance matrix to a numpy array
    distance_matrix_nparr = np.array(distance_matrix)

# Dump the numpy array to a file
with open("data/distance_matrix.npy", "wb") as f:
    np.save(f, distance_matrix_nparr)
