import pandas as pd
import numpy as np
import sys
import os

def topsis():
    if len(sys.argv) != 5:
        print("Usage: topsis <InputFile> <Weights> <Impacts> <OutputFile>")
        sys.exit(1)

    input_file = sys.argv[1]
    weights = sys.argv[2]
    impacts = sys.argv[3]
    output_file = sys.argv[4]

    if not os.path.isfile(input_file):
        print("Error: Input file not found")
        sys.exit(1)

    data = pd.read_csv(input_file)

    if data.shape[1] < 3:
        print("Error: Input file must contain at least 3 columns")
        sys.exit(1)

    try:
        criteria = data.iloc[:, 1:].astype(float)
    except:
        print("Error: Criteria columns must be numeric")
        sys.exit(1)

    weights = weights.split(",")
    impacts = impacts.split(",")

    if len(weights) != criteria.shape[1] or len(impacts) != criteria.shape[1]:
        print("Error: Number of weights, impacts, and criteria columns must match")
        sys.exit(1)

    try:
        weights = np.array(weights, dtype=float)
    except:
        print("Error: Weights must be numeric")
        sys.exit(1)

    for i in impacts:
        if i not in ["+", "-"]:
            print("Error: Impacts must be '+' or '-'")
            sys.exit(1)

    norm = np.sqrt((criteria ** 2).sum())
    normalized = criteria / norm
    weighted = normalized * weights

    ideal_best = []
    ideal_worst = []

    for i in range(weighted.shape[1]):
        if impacts[i] == "+":
            ideal_best.append(weighted.iloc[:, i].max())
            ideal_worst.append(weighted.iloc[:, i].min())
        else:
            ideal_best.append(weighted.iloc[:, i].min())
            ideal_worst.append(weighted.iloc[:, i].max())

    ideal_best = np.array(ideal_best)
    ideal_worst = np.array(ideal_worst)

    dist_best = np.sqrt(((weighted - ideal_best) ** 2).sum(axis=1))
    dist_worst = np.sqrt(((weighted - ideal_worst) ** 2).sum(axis=1))

    score = dist_worst / (dist_best + dist_worst)
    rank = score.rank(ascending=False, method="dense")

    data["Topsis Score"] = score
    data["Rank"] = rank.astype(int)

    data.to_csv(output_file, index=False)