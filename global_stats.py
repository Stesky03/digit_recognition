import json
import os
from pathlib import Path
import numpy as np

from preprocess_dataset import utility

def calculate_stats(input_path, output_file):
    average = utility.average_GAP(input_path)
    data = {"average": average.tolist(), "variance": utility.variance_GAP(input_path, average).tolist()}
    json.dump(data, open(output_file, "w"))
    base_path = Path(input_path)


input_path = Path("../../processed_fonts")
output_file = "stats.json"
calculate_stats(input_path, output_file)