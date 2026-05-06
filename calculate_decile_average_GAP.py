import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

import numpy as np

from preprocess_dataset.utility import extract_GAP
from preprocess_dataset.utility import average_GAP

def process_decile(decile_dir):
    # calculate and save average
    average_vector = average_GAP(decile_dir)
    json_path = decile_dir / "average_GAP.json"
    try:
        with open(json_path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"average": []}
    data["average"] = list(average_vector)
    with open(json_path, "w") as f:
        json.dump(data, f)

    # calculate and save all the similarity_from_average values (dot product)
    for subdir in [d for d in decile_dir.iterdir() if d.is_dir()]:
        similarity = np.dot(extract_GAP(subdir), average_vector)
        json_path = subdir / "stats.json"
        with open(json_path, "r") as f:
            data = json.load(f)
        data["similarity"] = similarity
        with open(json_path, "w") as f:
            json.dump(data, f)


def main():
    input_base = Path("../../processed_fonts_deciles")

    # Target specific decile1...decile10 directories
    decile_dirs = [input_base / f"decile_{i}" for i in range(1, 11)]

    # 10 workers to map 1:1 with the decile folders
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(process_decile, d_dir)
            for d_dir in decile_dirs if d_dir.is_dir()
        ]

        for future in futures:
            future.result()


if __name__ == "__main__":
    main()