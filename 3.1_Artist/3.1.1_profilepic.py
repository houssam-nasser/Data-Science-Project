import cv2
import os


def detect_face(image_path):
    """
    Detects if a face is present in an image using Haar cascades.

    Args:
        image_path: Path to the image file.

    Returns:
        True if at least one face is detected, False otherwise.
        Returns None on error.
    """
    try:
        # --- Load the pre-trained Haar cascade classifier ---
        # OpenCV provides pre-trained classifiers for face detection.
        # We'll use the 'haarcascade_frontalface_default.xml' classifier.

        # --- Robust way to locate the cascade file ---
        # This handles cases where the script might be run from different directories.
        cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        if not os.path.exists(cascade_path):
            raise FileNotFoundError("Haar cascade file not found.  Check your OpenCV installation.")
        face_cascade = cv2.CascadeClassifier(cascade_path)

        # --- Load the image ---
        img = cv2.imread(image_path)
        if img is None:  # Check if image loading was successful
            raise FileNotFoundError(f"Could not open or read image file: {image_path}")

        # --- Convert to grayscale ---
        # Haar cascades work on grayscale images.
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # --- Detect faces ---
        # The `detectMultiScale` function returns a list of rectangles,
        # where each rectangle represents a detected face.
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,  # Scale factor: How much the image size is reduced at each image scale.
            minNeighbors=5,
            # minNeighbors: How many neighbors each candidate rectangle should have to retain it.  Higher value = fewer false positives.
            minSize=(30, 30)  # minSize: Minimum possible object size. Objects smaller than that are ignored.
        )

        # --- Return True if at least one face is detected ---
        return len(faces) > 0

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return None
    except cv2.error as e:  # Handle OpenCV-specific errors
        print(f"OpenCV error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


print(detect_face('1. ProfilePicture/face_img.jpg'))
print(detect_face('1. ProfilePicture/fake_face.jpeg'))
print(detect_face('1. ProfilePicture/house.jpeg'))

