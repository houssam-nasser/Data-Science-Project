from PIL import Image
import numpy as np
from collections import Counter
# ... (other functions: rgb_to_hsv, hue_distance, etc. - from harmony code) ...

def dominant_color_proportions(image_path, num_dominant_colors=5):
    """
    Calculates the proportions of the image occupied by the dominant colors.

    Args:
        image_path: Path to the image file.
        num_dominant_colors: The number of dominant colors to consider.

    Returns:
        A dictionary where keys are RGB tuples (representing the
        dominant colors) and values are floats (0.0-1.0) representing
        the proportion of the image occupied by that color.
        Returns None on error.
    """
    try:
        img = Image.open(image_path).convert("RGB")
        pixels = np.array(img).reshape(-1, 3)

        counts = Counter(map(tuple, pixels))  # 2. Count occurrences of each unique color
        sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        dominant_colors = [color for color, count in sorted_counts[:num_dominant_colors]]

        total_pixels = pixels.shape[0]
        proportions = {}
        for color in dominant_colors:
            proportions[color] = counts[color] / total_pixels

        return proportions

    except Exception as e:
        print(f"Error processing image: {e}")
        return None


if __name__ == '__main__':
    image_path = "your_image.jpg"  # Replace with your image
    proportions = dominant_color_proportions(image_path)
    if proportions:
        for color, prop in proportions.items():
            print(f"Color: {color}, Proportion: {prop:.4f}")