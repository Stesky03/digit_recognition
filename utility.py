import json

import numpy as np


def extract_GAP(font_dir):
    json_path = font_dir / "stats.json"
    try:
        with open(json_path, "r") as f:
            data = json.load(f)
            if "GAP" in data:
                return np.array(data["GAP"])
            else:
                return 0

    except  FileNotFoundError:
        return 0

def extract_standard_GAP(font_dir):
    json_path = font_dir / "stats.json"
    try:
        with open(json_path, "r") as f:
            data = json.load(f)
            if "GAP" in data:
                return np.array(data["standard_GAP"])
            else:
                return 0

    except  FileNotFoundError:
        return 0


def average_GAP(dir):
    sum_vector = np.zeros(shape = 512, dtype = np.float64)
    i = 0

    # sum all the GAPs
    for subdir in [d for d in dir.iterdir() if d.is_dir()]:
        sum_vector += extract_GAP(subdir)
        i+=1
        print(f"{subdir} completed")

    if i == 0:
        print(f"{dir.name} is empty!")
        return 0;
    else:
        print(f"{dir.name} completed.")
    return sum_vector / i

def variance_GAP(dir, average_vector):
    sum_vector = np.zeros(shape = 512, dtype = np.float64)
    i = 0

    # sum all the GAPs
    for subdir in [d for d in dir.iterdir() if d.is_dir()]:
        sum_vector += (extract_GAP(subdir) - average_vector) ** 2
        i+=1
        print(f"{subdir} completed")

    if i <= 1:
        print(f"{dir.name} is empty!")
        return 0;
    else:
        print(f"{dir.name} completed.")
    return sum_vector / (i-1)
