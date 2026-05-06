import json
import os
import shutil
from pathlib import Path


def filter_by_black_score(font_path):
    colored_pixels = 0.0
    with open(Path(font_path) / "stats.json", "r") as file:
        data = json.load(file)
        colored_pixels = data["black_score"]
        at_least_one_empty_file = data["empty_file"]
    if at_least_one_empty_file or colored_pixels >= 0.4:
        #remove the fonts that have 0 or too many black pixels
        shutil.rmtree(font_path)



work_dir = Path("../../allFonts_selection")
i = 0
for f in os.listdir(work_dir):
    full_path = work_dir / f
    if full_path.is_dir():
        filter_by_black_score(full_path)

    print(f"Processati: {i}")
    i += 1

print("\nElaborazione completata!")