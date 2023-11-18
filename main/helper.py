import math
import numpy as np

from PIL import Image


# Get the closest color
def rgb_to_xyz(rgb):
    # Convert RGB to CIE 1931 XYZ color space
    r, g, b = [x / 255.0 for x in rgb]
    r = _gamma_correction(r)
    g = _gamma_correction(g)
    b = _gamma_correction(b)

    r = _srgb_to_xyz(r)
    g = _srgb_to_xyz(g)
    b = _srgb_to_xyz(b)

    x = r * 0.4124564 + g * 0.3575761 + b * 0.1804375
    y = r * 0.2126729 + g * 0.7151522 + b * 0.0721750
    z = r * 0.0193339 + g * 0.1191920 + b * 0.9503041

    return x, y, z


def _gamma_correction(value):
    if value <= 0.04045:
        return value / 12.92
    else:
        return ((value + 0.055) / 1.055) ** 2.4


def _srgb_to_xyz(value):
    if value <= 0.04045:
        return value / 12.92
    else:
        return ((value + 0.055) / 1.055) ** 2.4


def delta_e_cie76(color1, color2):
    # Calculate the Euclidean distance between two colors in the CIE 1931 XYZ color space
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(color1, color2)))


def closest_color(target, color_set):
    # Find the color in color_set that is closest to the target color
    target_xyz = rgb_to_xyz(target)
    min_distance = float('inf')
    closest = None

    for color in color_set:
        color_xyz = rgb_to_xyz(color)
        distance = delta_e_cie76(target_xyz, color_xyz)

        if distance < min_distance:
            min_distance = distance
            closest = color

    return closest

# Example usage:
target_color = (125, 200, 75)  # RGB color to match
limited_color_set = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # Limited set of colors

closest = closest_color(target_color, limited_color_set)
# print(f"The closest color is: {closest}")


def get_median_color(image_path):
    # Open the image
    image = Image.open(image_path)

    # Resize the image to 16x16 pixels
    image = image.resize((16, 16))

    # Convert the image to a NumPy array
    image_array = np.array(image)

    # Reshape the array to a flat list of RGBA values
    pixels = image_array.reshape((-1, 4))

    # Calculate the median RGBA values
    median_color = np.median(pixels, axis=0).astype(int)

    return tuple(median_color)
