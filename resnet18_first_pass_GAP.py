import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

import torch
from torchvision import models
from PIL import Image

import numpy as np

# Load model and strip the final classification layer
model = models.resnet18(weights='DEFAULT')
model = torch.nn.Sequential(*list(model.children())[:-1]).eval()
preprocess = models.ResNet18_Weights.DEFAULT.transforms()

#returns the list of the 512 numbers of GAP
def extract_vector(path):
    with torch.no_grad():
        # .convert('RGB') duplicates the channel
        img = Image.open(path).convert('RGB')
        vect = model(preprocess(img).unsqueeze(0)).flatten()
        normalized_vect = vect / np.linalg.norm(vect)
        return normalized_vect.tolist()


def process_font_grid(font_dir):
    json_path = font_dir / "stats.json"
    try:
        with open(json_path, "r") as f:
            data = json.load(f)
            if "GAP" in data:
                print(f"{font_dir} already processed, skipping")
                return

    except  FileNotFoundError:
        data = {"GAP": []}

    font_image = Path(font_dir) / "grid.png"
    result_list = extract_vector(font_image)
    data["GAP"] = result_list

    with open(json_path, "w") as f:
        json.dump(data, f)


def process_decile(decile_dir):
    for subdir in [d for d in decile_dir.iterdir() if d.is_dir()]:
        process_font_grid(subdir)
        print(f"{subdir} completed")
    print(f"Thread for {decile_dir.name} completed.")


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