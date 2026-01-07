from PIL import Image
import numpy as np

def image_colorfulness(image_path):
    """
    Calculates the colorfulness of an image using the Hasler and
    Süsstrunk method. Measure of the intensity and vibrancy of colors in an image.

    Args:
        image_path: Path to the image file.

    Returns:
        A float representing the colorfulness. Higher values indicate
        more colorful images. Returns None on error.
    """
    try:
        img = Image.open(image_path).convert("RGB")
        pixels = np.array(img).reshape(-1, 3)

        # Calculate rg and yb (as defined in the paper)
        r, g, b = pixels[:, 0], pixels[:, 1], pixels[:, 2]
        rg = np.abs(r - g)
        yb = np.abs(0.5 * (r + g) - b)

        # Calculate mean and standard deviation of rg and yb
        (rg_mean, rg_std) = (np.mean(rg), np.std(rg))
        (yb_mean, yb_std) = (np.mean(yb), np.std(yb))

        # Combine the mean and standard deviation
        std_root = np.sqrt((rg_std ** 2) + (yb_std ** 2))
        mean_root = np.sqrt((rg_mean ** 2) + (yb_mean ** 2))

        colorfulness = std_root + (0.3 * mean_root)
        return colorfulness

    except Exception as e:
        print(f"Error processing image: {e}")
        return None