from PIL import Image
import numpy as np


def image_warmth(image_path):
    """
    Calculates a warmth score for an image, scaled from 0 (coolest) to 100(warmest).

    Args:
        image_path: Path to the image file.

    Returns:
        A float between 0.0 and 100.0:
        -   0.0 represents an extremely cool image.
        -  50.0 represents a neutral image (balanced warm and cool).
        - 100.0 represents an extremely warm image.
        Returns None on error.
    """
    try:
        img = Image.open(image_path).convert("RGB")
        pixels = np.array(img).reshape(-1, 3)

        r, g, b = pixels[:, 0], pixels[:, 1], pixels[:, 2]

        # More robust warmth/coolness calculation
        warmth = r - (g + b) / 2
        coolness = b - (r + g) / 2

        warmth_coolness_score = np.mean(warmth - coolness)

        # Normalize
        max_abs_score = 255  # Maximum absolute value the score could have
        normalized_score = warmth_coolness_score / max_abs_score

        # Scale and shift to 0-100 range
        scaled_score = (normalized_score + 1.0) * 50.0

        # Clip to 0-100 (important for edge cases)
        scaled_score = np.clip(scaled_score, 0.0, 100.0)

        return scaled_score

    except Exception as e:
        print(f"Error processing image: {e}")
        return None


print(image_warmth('Color/1. Warmth/cool.jpeg'))
print(image_warmth('Color/1. Warmth/warm.jpeg'))
print(image_warmth('Color/original.jpg'))