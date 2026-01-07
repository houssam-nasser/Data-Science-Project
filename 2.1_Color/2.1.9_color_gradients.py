from PIL import Image
import numpy as np
from scipy.signal import convolve2d

def color_gradient_magnitude(image_path):
    """
    Calculates the average magnitude of color gradients in an image
    using the Sobel operator.

    Args:
        image_path: Path to the image file.

    Returns:
        A float representing the average gradient magnitude. Higher
        values indicate stronger color edges.  Returns None on error.
    """
    try:
        img = Image.open(image_path).convert("RGB")
        pixels = np.array(img).astype(np.float64)  # Use float64 for calculations

        # Sobel kernels (horizontal and vertical)
        sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
        sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

        gradient_magnitude_sum = 0.0

        # Apply Sobel operator to each color channel separately
        for channel in range(3):  # R, G, B
            channel_data = pixels[:, :, channel]

            # Convolve with Sobel kernels
            gradient_x = convolve2d(channel_data, sobel_x, mode='same', boundary='symm')
            gradient_y = convolve2d(channel_data, sobel_y, mode='same', boundary='symm')

            # Calculate gradient magnitude
            gradient_magnitude = np.sqrt(gradient_x**2 + gradient_y**2)
            gradient_magnitude_sum += np.mean(gradient_magnitude)

        # Average gradient magnitude across all channels
        avg_gradient_magnitude = gradient_magnitude_sum / 3.0
        return avg_gradient_magnitude

    except Exception as e:
        print(f"Error processing image: {e}")
        return None