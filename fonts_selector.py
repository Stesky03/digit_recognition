import os
from fontTools.ttLib import TTFont

def delete_font(font, path):
    font.close()
    print(f"Deleting {path}")
    if os.path.exists(path):
        os.remove(path)

def remove_nondigit_fonts(fonts_path, font_name):
    try:
        full_path = os.path.join(fonts_path, font_name)
        
        # do not handle subdirs, it's not worth it, we already have a lot of fonts
        if os.path.isdir(full_path):
            return
        
        font = TTFont(full_path)
        # Get the 'cmap' table
        cmap_table = font['cmap']
        # fonttools' getBestCmap() handles selection logic automatically
        cmap = cmap_table.getBestCmap()
        if cmap is None:
            #font.close()
            delete_font(font, full_path)
            return

        for i in range(10):
            unicode_val = 0x30 + i  # ASCII/Unicode '0'-'9'
            glyph_name = cmap.get(unicode_val)
            # filter out fonts with no digits
            if glyph_name is None:
                #font.close();
                delete_font(font, full_path)
                break
        
        font.close()


    except Exception as e:
        print(f"Error processing font: {e}")


path = "../../allFonts"

for name in os.listdir(path):
    remove_nondigit_fonts(path, name)