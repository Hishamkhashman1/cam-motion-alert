import cv2

from config import FRAME_WIDTH

"""TODO: Resize and normalize frames before motion comparison."""

# TODO: Resize frames to the configured width while preserving aspect ratio.
# TODO: Convert frames to grayscale and apply blur for stable motion detection.

def preprocess_frame(frame):
    height, width = frame.shape[:2]
    resized_height = int(height * FRAME_WIDTH / width)
    resized = cv2.resize(frame, (FRAME_WIDTH, resized_height))
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    return resized, gray

