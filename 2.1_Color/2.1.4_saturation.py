from PIL import Image
import numpy as np


def image_saturation_score(image_path, target_saturation=0.6, std_dev=0.25):
    """
    Calculates an image saturation score, favoring a specified target saturation.

    Args:
        image_path: Path to the image file.
        target_saturation: The ideal saturation level (0.0 to 1.0). Default: 0.6
        std_dev: The standard deviation for the Gaussian scoring function.
                 Larger values are more lenient. Default: 0.25

    Returns:
        A float between 0.0 and 100.0, where higher scores indicate better
        saturation (closer to the target saturation level).  Returns None on
        error.
    """
    try:
        img = Image.open(image_path).convert("RGB")
        pixels = np.array(img).reshape(-1, 3)

        # Convert RGB to HSV
        pixels_float = pixels.astype(np.float64) / 255.0
        r, g, b = pixels_float[:, 0], pixels_float[:, 1], pixels_float[:, 2]

        max_c = np.maximum(np.maximum(r, g), b)
        min_c = np.minimum(np.minimum(r, g), b)
        diff = max_c - min_c

        h = np.zeros_like(r)
        s = np.zeros_like(r)
        v = max_c

        # Calculate Hue (handle division by zero by preventing it)
        non_zero_diff = diff != 0  # Boolean mask for non-zero diff

        # Calculate Hue *only* where diff is not zero
        h_r = (max_c == r) & non_zero_diff
        h[h_r] = (60 * ((g[h_r] - b[h_r]) / diff[h_r]) + 360) % 360
        h_g = (max_c == g) & non_zero_diff
        h[h_g] = (60 * ((b[h_g] - r[h_g]) / diff[h_g]) + 120) % 360
        h_b = (max_c == b) & non_zero_diff
        h[h_b] = (60 * ((r[h_b] - g[h_b]) / diff[h_b]) + 240) % 360

        # Calculate 4. Saturation (handle division by zero by preventing it)
        non_zero_max_c = max_c != 0  # Boolean mask for non-zero max_c
        s[non_zero_max_c] = diff[non_zero_max_c] / max_c[non_zero_max_c]

        # Calculate average saturation
        avg_saturation = np.mean(s)

        # --- Scoring Function (Gaussian) ---
        score = 100 * np.exp(-((avg_saturation - target_saturation) ** 2) / (2 * std_dev ** 2))

        return score

    except FileNotFoundError:
        print(f"Error: File not found at {image_path}")
        return None
    except OSError:
        print(f"Error: Could not open or read image file at {image_path}")
        return None
    except Exception as e:
        print(f"Error processing image: {e}")  # More specific error message
        return None


print("colors - ", image_saturation_score('Color/5. Brightness/normal.jpg'))
print("saturated - ", image_saturation_score('Color/4. Saturation/sat_normal.png'))