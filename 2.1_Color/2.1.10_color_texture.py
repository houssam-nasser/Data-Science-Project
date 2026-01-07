from PIL import Image
import numpy as np
from scipy.signal import convolve2d

def color_texture(image_path):
    """
    Calculates a measure of color texture based on the standard
    deviation of the gradient magnitude.

    Args:
        image_path: Path to the image file.

    Returns:
        A float representing the color texture. Higher values indicate
        more textured color variations. Returns None on error.
    """
    try:
        img = Image.open(image_path).convert("RGB")
        pixels = np.array(img).astype(np.float64)

        sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
        sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

        gradient_magnitudes = []

        for channel in range(3):
            channel_data = pixels[:, :, channel]
            gradient_x = convolve2d(channel_data, sobel_x, mode='same', boundary='symm')
            gradient_y = convolve2d(channel_data, sobel_y, mode='same', boundary='symm')
            gradient_magnitude = np.sqrt(gradient_x**2 + gradient_y**2)
            gradient_magnitudes.append(gradient_magnitude)

        # Combine gradient magnitudes from all channels
        combined_gradient_magnitude = np.mean(np.stack(gradient_magnitudes), axis=0)

        # Calculate the standard deviation of the combined gradient magnitude
        texture_measure = np.std(combined_gradient_magnitude)
        return texture_measure

    except Exception as e:
        print(f"Error processing image: {e}")
        return None

