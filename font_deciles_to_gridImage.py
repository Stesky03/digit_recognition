import shutil
import threading
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageFont, ImageDraw

# Lock required for thread-safe writes to the shared error log
error_lock = threading.Lock()


def process_font(font_path, img_size=(224, 224), font_size=64):
    W, H = img_size
    cols, rows = 3, 4
    cell_w, cell_h = W // cols, H // rows

    font_name = font_path.stem
    print(f"font path: {font_path}")

    try:
        font = ImageFont.truetype(str(font_path), font_size)

        img = Image.new('L', img_size, color=255)
        draw = ImageDraw.Draw(img)

        for digit in range(10):
            char = str(digit)
            bbox = font.getbbox(char)
            if not bbox or (bbox[2] - bbox[0] == 0):
                raise ValueError("Missing or zero-width glyph")

            col = digit % cols
            row = digit // cols
            center_x = (col * cell_w) + (cell_w // 2)
            center_y = (row * cell_h) + (cell_h // 2)

            draw.text((center_x, center_y), char, font=font, fill=0, anchor="mm")

        print("final image: " + str(font_path.parent / "grid.png"))
        img.save(font_path.parent / "grid.png")
    except Exception as e:
        return



def process_decile(decile_dir):
    font_files = list(Path(decile_dir).glob("**/*.[ot]tf"))
    for font_path in font_files:
        process_font(font_path)
    print(f"Thread for {decile_dir.name} completed. Processed {len(font_files)} fonts.")


def main():
    input_base = Path("../../processed_fonts_deciles")

    # Target specific decile1...decile10 directories
    decile_dirs = [input_base / f"decile_{i}" for i in range(1, 11)]

    with open("../broken_fonts_list.txt", "w") as error_log:
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