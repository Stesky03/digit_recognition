import shutil
from pathlib import Path
from PIL import Image, ImageFont, ImageDraw

def process_font_library(font_list, base_output_dir, error_file, suffix, img_size=(224, 224), font_size=100):
    base_path = Path(base_output_dir)
    W, H = img_size
    center = (W // 2, H // 2)
    counter = 0

    for font_path in map(Path, font_list):
        # 1. Setup Directory Structure
        font_name = font_path.stem
        font_root = base_path / font_name
        # print(font_root)

        try:
            # Verify font validity before creating folders
            font = ImageFont.truetype(str(font_path), font_size)

            # copy the original font file
            font_root.mkdir(parents=True, exist_ok=True)
            shutil.copy2(font_path, font_root / f"font{font_path.suffix}")

        except Exception as e:
            error_file.write(font_path.name + "\n")
            continue

        try:
            # 2. Render Digits
            for digit in range(10):
                char = str(digit)

                # Skip if glyph is missing (bbox returns None or zero-width)
                bbox = font.getbbox(char)
                if not bbox or (bbox[2] - bbox[0] == 0):
                    error_file.write(font_path.name + "\n")
                    break

                # Create digit-specific subdirectories
                digit_dir = font_root / char
                # if digit_dir.exists(): #comment this lines to regenerate images
                    #continue
                    
                digit_dir.mkdir(exist_ok=True)

                # Render to fixed-size canvas
                img = Image.new('L', img_size, color=255)
                draw = ImageDraw.Draw(img)

                # 'mm' anchor handles the vertical/horizontal centering logic
                draw.text(center, char, font=font, fill=0, anchor="mm")

                # Save as PNG (lossless)
                img.save(digit_dir / f"{char}{suffix}.png")

        except OSError as e:
            error_file.write(font_path.name + "\n")
            continue

        print(f"{counter}")
        counter += 1


# Usage
fonts_path = Path("../../allFonts")
#fonts_path = Path("test_fonts")
font_files = list(fonts_path.glob("**/*.[ot]tf"))

output_path = Path("../../allFonts_selection")
#output_path = Path("test_output")
process_font_library(font_files, output_path, error_file = open("../broken_fonts_list.txt", "w"), suffix="", img_size=(224, 224))