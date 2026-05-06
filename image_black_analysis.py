import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from PIL import Image, ImageStat
import json

def update_json(json_path, white_counter, empty_file):
    if json_path.exists():
        with open(json_path, "r") as file:
            data = json.load(file)
    else:
        data = {}

    # Aggiorno il valore
    data["black_score"] = white_counter
    data["empty_file"] = empty_file

    with open(json_path, "w") as file:
        json.dump(data, file, indent=4)


def get_weighted_black(image_path):
    if not image_path.exists():
        return 0.0
    try:
        with Image.open(image_path).convert('L') as img:
            stat = ImageStat.Stat(img)
            # returns 0 if the image is only white (empty), 1.0 if all black
            # 12.25 is the ratio between size of the digit and the size of the canvas
            return (1.0 - (stat.mean[0] / 255.0)) * 12.25
    except Exception:
        return 0.0

def process_single_font(font_path):
    base_path = Path(font_path)

    black_score = 0
    empty_file = False
    for i in range(10):
        image_path = base_path.joinpath(f"{i}/{i}.png")
        weighted_black_score = get_weighted_black(image_path)
        if weighted_black_score == 0.0:
            empty_file = True
        black_score += get_weighted_black(image_path)

    update_json(base_path / "stats.json", black_score / 10, empty_file)


work_dir = Path("../../allFonts_selection")

font_paths = []
for f in os.listdir(work_dir):
    full_path = work_dir / f
    if full_path.is_dir():  # Più pulito di is_file -> continue
        font_paths.append(full_path)

with ThreadPoolExecutor(max_workers=None) as executor:
    results = executor.map(process_single_font, font_paths)

    for i, _ in enumerate(results, 1):
        print(f"Processati: {i}")

print("\nElaborazione completata!")

