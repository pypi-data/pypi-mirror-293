from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt
from optirustic import NSGA3

# Generate a 3D Pareto front charts and objective vs. reference point charts
file = (
    Path(__file__).parent.parent
    / "examples"
    / "results"
    / "DTLZ1_3obj_Adaptive_NSGA3_gen400.json"
)
data = NSGA3(file.as_posix())
r = [
    ind.data["reference_point"]
    for ind in data.individuals
    if ind.data["reference_point_index"] > 92
]
rx = [
    ind.data["reference_point_index"]
    for ind in data.individuals
    if ind.data["reference_point_index"] > 92
]
r = np.array(r)
for i in range(3):
    print(r[:, i].min(), r[:, i].max())

for ri, r in enumerate(data.additional_data["reference_points"]):
    if all([coord <= 0.5 for coord in r]) and ri > 92:
        print(ri, r, ri in rx)
