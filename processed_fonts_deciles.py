import os
import json
import shutil
import math
from pathlib import Path


def organize_fonts_by_decile(source_dir, output_dir):
    source_path = Path(source_dir)
    output_path = Path(output_dir)
    font_data = []


    # 1. Collect scores and file paths
    for subdir in [d for d in source_path.iterdir() if d.is_dir()]:
        stats_file = subdir / "stats.json"


        if stats_file.exists():
            try:
                with open(stats_file, 'r') as f:
                    stats = json.load(f)
                    score = stats.get("black_score")

                if score is not None:
                    font_data.append({
                        "path": subdir,
                        "black_score": float(score)
                    })
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Skipping {subdir}: {e}")

    # 2. Sort by score
    font_data.sort(key=lambda x: x["black_score"])

    total_fonts = len(font_data)
    if total_fonts == 0:
        print("No valid font/stats pairs found.")
        return

    # 3. Distribute into deciles
    for index, path in enumerate(font_data):
        # Calculate decile (1-10)
        decile = (index * 10 // total_fonts) + 1

        target_folder = output_path / f"decile_{decile}" / path["path"].name
        target_folder.mkdir(parents=True, exist_ok=True)

        font_files = list(path["path"].glob("*.ttf")) + list(path["path"].glob("*.otf"))
        new_filename = path["path"].name + font_files[0].suffix

        shutil.copy2(font_files[0], target_folder / new_filename)

    print(f"Processed {total_fonts} fonts into {output_path}")


    # Configure your paths here
SOURCE = "../../allFonts_selection"
DESTINATION = "../../processed_fonts_deciles"

organize_fonts_by_decile(SOURCE, DESTINATION)