import cv2
import time
from datetime import datetime

import config
import notifier
import preprocessing
import snapshots

"""TODO: Implement the motion detection loop that reads frames, detects motion, saves snapshots, and sends alerts."""

# TODO: Open the RTSP stream and read successive frames.
# TODO: Preprocess frames, compare them, and detect contours above the configured motion threshold.
# TODO: Throttle alerts using the cooldown setting.
# TODO: Save snapshots and send WhatsApp notifications when motion is detected.
# TODO: Release the camera and close OpenCV windows on exit.
