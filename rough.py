from PIL import Image


def get_image_dimensions(image_path):
    """
    Gets the dimensions (width and height) of an image.

    Args:
        image_path: The path to the image file.

    Returns:
        A tuple (width, height) representing the image dimensions,
        or None if the image cannot be opened.  Returns -1, -1 on error.
    """
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            return width, height
    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
        return -1, -1  # Or raise the exception, depending on your needs
    except (IOError, OSError) as e:  # Catch potential PIL errors
        print(f"Error: Could not open or read image file: {e}")
        return -1, -1
    except Exception as e:  # Catch any other potential exceptions.
        print(f"An unexpected error occurred: {e}")
        return -1, -1


def get_image_dimensions_cv2(image_path):
    """Gets image dimensions using OpenCV.  More robust handling of corrupted files."""
    import cv2  # Import inside the function to avoid unnecessary dependency if not used.

    try:
        img = cv2.imread(image_path)
        if img is None:  # Crucial check: cv2.imread returns None if it fails
            print(f"Error: Could not read image file at {image_path} (cv2.imread returned None)")
            return -1, -1
        height, width, _ = img.shape  # '_' discards the number of channels
        return width, height
    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
        return -1, -1
    except Exception as e:
        print(f"An unexpected error occurred with OpenCV: {e}")
        return -1, -1


if __name__ == '__main__':
    # Example usage:
    image_file = "/2.1_Color/Color/original.jpg"  # Replace with the actual path to your image
    img = "/Users/vibhu/PycharmProjects/art_proj/Test Cases/Color/3. Percent Colored/complimentary.png"
    # --- Using PIL ---
    width, height = get_image_dimensions(img)

    if width != -1:
        print(f"Image dimensions (PIL): Width = {width}, Height = {height}")
