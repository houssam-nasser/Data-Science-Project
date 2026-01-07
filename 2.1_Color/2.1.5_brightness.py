from PIL import Image
import numpy as np

# Adjust the parameter of target brightness
# Our aim will be to find the brighteness that yields the most money

def image_brightness_score(image_path, target_brightness=0.65, std_dev=0.25):
    """
    Calculates an image brightness score, favoring a specified target brightness.

    Args:
        image_path: Path to the image file.
        target_brightness: The ideal brightness level (0.0 to 1.0). Default: 0.5
        std_dev: Standard deviation for the Gaussian. Larger = more lenient.

    Returns:
        A float between 0.0 and 100.0. Higher scores are closer to the target.
        Returns None on error.
    """
    try:
        img = Image.open(image_path).convert("RGB")
        pixels = np.array(img).reshape(-1, 3)

        # --- HSV Conversion (Efficient & Correct) ---
        pixels_float = pixels.astype(np.float64) / 255.0
        r, g, b = pixels_float[:, 0], pixels_float[:, 1], pixels_float[:, 2]
        max_c = np.maximum(np.maximum(r, g), b)
        min_c = np.minimum(np.minimum(r, g), b)
        diff = max_c - min_c
        h = np.zeros_like(r)
        s = np.zeros_like(r)
        v = max_c  # Value (5. Brightness) is simply the maximum channel
        non_zero_diff = diff != 0
        h[max_c == min_c] = 0
        h_r = np.where((max_c == r) & non_zero_diff)
        h[h_r] = (60 * ((g[h_r] - b[h_r]) / diff[h_r]) + 360) % 360
        h_g = np.where((max_c == g) & non_zero_diff)
        h[h_g] = (60 * ((b[h_g] - r[h_g]) / diff[h_g]) + 120) % 360
        h_b = np.where((max_c == b) & non_zero_diff)
        h[h_b] = (60 * ((r[h_b] - g[h_b]) / diff[h_b]) + 240) % 360
        s = np.where(max_c != 0, diff / max_c, 0)

        # --- Average 5. Brightness ---
        avg_brightness = np.mean(v)

        # --- Gaussian Scoring ---
        score = 100 * np.exp(-((avg_brightness - target_brightness) ** 2) / (2 * std_dev ** 2))
        return score

    except Exception as e:
        print(f"Error processing image: {e}")
        return None

print("Colors  ", image_brightness_score('Color/5. Brightness/normal.jpg'))
print("Too bright ", image_brightness_score('Color/5. Brightness/inc_normal.png'))
print("Less bright ", image_brightness_score('Color/5. Brightness/dec_normal.png'))