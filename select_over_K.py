import shutil
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import json

def process_decile(decile_dir, output_dir, k):
    for subdir in [d for d in decile_dir.iterdir() if d.is_dir()]:
        json_path = subdir / "stats.json"
        with open(json_path, "r") as f:
            data = json.load(f)
        if data["similarity"] > k:
            shutil.copytree(subdir, output_dir / subdir.name, dirs_exist_ok=True)


def main():
    input_base = Path("../../processed_fonts_deciles")
    output_base = Path("../../processed_fonts_2")

    # remove directories over decile7
    decile_dirs = [input_base / f"decile_{i}" for i in range(1, 8)]

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(process_decile, d_dir, output_base, 0.85)
            for d_dir in decile_dirs if d_dir.is_dir()
        ]

        for future in futures:
            future.result()


if __name__ == "__main__":
    main()