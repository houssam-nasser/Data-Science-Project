from PIL import Image
import numpy as np

# NOT WORKING ~~~~~~~~~~

def percent_colored(image_path, tolerance=10):
    """
    Calculates the percentage of color in an image, allowing for a tolerance.

    Args:
        image_path: Path to the image file.
        tolerance:  Maximum difference between R, G, and B values (and A if present)
                    for a pixel to be considered grayscale.  Defaults to 10.

    Returns:
        The color percentage as a float.
        Returns None if there's an error opening the image.
        Returns -1 if the image doesn't have 3 or 4 channels.
    """
    try:
        img = Image.open(image_path)
        img_array = np.array(img)

        if len(img_array.shape) < 3:
            return -1  # Not a color image (or has unsupported dimensions)

        num_channels = img_array.shape[2]
        if num_channels < 3 or num_channels > 4:
            return -1  # Only support 3 or 4 channel images

        r = img_array[:, :, 0]
        g = img_array[:, :, 1]
        b = img_array[:, :, 2]

        grayscale_pixels = (np.abs(r - g) <= tolerance) & (np.abs(g - b) <= tolerance) & (np.abs(r - b) <= tolerance)

        if num_channels == 4:
            a = img_array[:, :, 3]
            grayscale_pixels = grayscale_pixels & (a >= 255 - tolerance)

        num_grayscale = np.sum(grayscale_pixels)
        total_pixels = img_array.shape[0] * img_array.shape[1]
        num_color = total_pixels - num_grayscale
        color_percent = (num_color / total_pixels) * 100
        return color_percent

    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
        return None
    except OSError:
        print(f"Error: Could not open or read image file at {image_path}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def main():
    # Example Usage (Corrected and Expanded)
    image_paths = [
        "cats_office.jpg",  #  Replace with the *actual* filenames
        "starry_night.jpg"
    ]
    tolerances = [0, 20, 50]  # Different tolerances to demonstrate

    for image_path in image_paths:
        print(f"Analyzing: {image_path}")
        for tolerance in tolerances:
            color_percent = percent_colored(image_path, tolerance)
            if color_percent is not None:
                if color_percent == -1:
                    print("  Image is not 3 or 4 channel")
                else:
                    print(f"  Tolerance {tolerance}: Color = {color_percent:.2f}%")
        print("-" * 20) #separator for readability



print(percent_colored('Color/3. Percent Colored/b&w.jpg'))
print(percent_colored('Color/3. Percent Colored/b&w_with_red.jpg'))
print(percent_colored('Color/3. Percent Colored/colored.jpg'))