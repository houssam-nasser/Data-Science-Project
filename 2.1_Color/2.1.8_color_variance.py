from PIL import Image
import numpy as np

def color_variance(image_path):
    """
    Calculates the variance of the R, G, and B channels.

    Args:
        image_path: Path to the image file.

    Returns:
        A tuple (r_var, g_var, b_var) representing the variance of
        the red, green, and blue channels, respectively. Returns None
        on error.
    """
    try:
        img = Image.open(image_path).convert("RGB")
        pixels = np.array(img).reshape(-1, 3)

        r_var = np.var(pixels[:, 0])
        g_var = np.var(pixels[:, 1])
        b_var = np.var(pixels[:, 2])

        return (r_var, g_var, b_var)

    except Exception as e:
        print(f"Error processing image: {e}")
        return None