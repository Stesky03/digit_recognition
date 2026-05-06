import json
from pathlib import Path

import numpy as np
from sklearn.decomposition import PCA

from preprocess_dataset.utility import *

def normalize(font_path, global_stats):
    json_path = font_path / "stats.json"
    with open(json_path) as f:
        data = json.load(f)
    base_GAP = data["GAP"]

    base_GAP_array = np.array(base_GAP)
    average_array = np.array(global_stats["average"])
    variance_array = np.array(global_stats["variance"])

    standardized_array = (base_GAP_array - average_array) / np.sqrt(variance_array)
    data["standard_GAP"] = standardized_array.tolist()
    json.dump(data, open(json_path, "w"))

def PCA_GAP(data):
    data = np.array(data)

    # keep 95% of the variance
    pca = PCA(n_components=0.95)

    # Fit and transform
    pca_result = pca.fit_transform(data)

    print(f"Original shape: {data.shape[1]}")
    print(f"Reduced shape: {pca_result.shape}")

    return pca_result

def forall_fonts(fonts_path, stats_path):
    global_stats = json.load(open(stats_path))
    all_GAPs = []
    all_standard_GAPs = []
    font_ID = []

    for font_path in fonts_path.iterdir():
        if font_path.is_dir():
            #normalize(font_path, global_stats)
            all_GAPs.append(extract_GAP(font_path))
            all_standard_GAPs.append(extract_standard_GAP(font_path))
            font_ID.append(font_path.name)

    pca_matrix = PCA_GAP(all_GAPs)
    PCA_GAP(all_standard_GAPs)

# save each resulting vector of the matrix to its font stats file
    for i in range(len(font_ID)):
        name = font_ID[i]
        vector = pca_matrix[i].tolist()

        font_dir = fonts_path / name
        json_path = font_dir / "stats.json"

        if json_path.exists():
            with open(json_path, "r") as f:
                data = json.load(f)

            data["PCA_GAP"] = vector

            with open(json_path, "w") as f:
                json.dump(data, f)

input_path = Path("../../processed_fonts")
stats_path = "stats.json"
forall_fonts(input_path, stats_path)