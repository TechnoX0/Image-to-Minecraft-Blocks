import os.path
import shutil

from PIL import Image
from helper import *
from pathlib import Path


def get_image_data(path):
    im = Image.open(path).convert("RGBA")
    width, height = im.size
    data = {
        "pixels": list(im.getdata()),
        "width": width,
        "height": height,
    }
    return data


folder_path = "D:/Dev/test/block"
filtered_folder_path = "D:/Dev/test/filtered blocks"


# Filters the block textures from minecraft
# Conditions for the filter:
#     The blocks should be 16x16 to make sure it's an actual block
#     It shouldn't have an alpa 0 value to make sure it's not transparent
def filter_minecraft_blocks(path):
    files = os.listdir(path)
    for file in files:
        path = folder_path + "/" + file
        try:
            data = get_image_data(path)
            has_tp = has_transparent(data["pixels"])
            if data["width"] == 16 and data["height"] == 16 and not has_tp:
                shutil.copy(path, filtered_folder_path)
        except:
            print("Error: " + path)


# This just checks if there's an alpha 0 value
def has_transparent(pixel_data):
    for pixel in pixel_data:
        if pixel[3] == 0:
            return True
    return False


def get_colors_from_blocks():
    pass


filter_minecraft_blocks(folder_path)
