import cv2
import time
from datetime import datetime

from config import ALERT_COOLDOWN_SECONDS
from config import MIN_CONTOUR_AREA
from config import RTSP_URL
from notifier import send_whatsapp_alert
from preprocessing import preprocess_frame
from snapshots import build_public_snapshot_url
from snapshots import save_snapshots



"""TODO: Implement the motion detection loop that reads frames, detects motion, saves snapshots, and sends alerts."""

# TODO: Open the RTSP stream and read successive frames.
# TODO: Preprocess frames, compare them, and detect contours above the configured motion threshold.
# TODO: Throttle alerts using the cooldown setting.
# TODO: Save snapshots and send WhatsApp notifications when motion is detected.
# TODO: Release the camera and close OpenCV windows on exit.

def run_motion_detector() -> None:
    cap = cv2.VideoCapture(RTSP_URL)
    if not cap.isOpened():
        raise RuntimeError("Could not open RTSP stream")

    ret1, frame1 = cap.read()
    ret2, frame2 = cap.read()

    if not ret1 or not ret2:
        cap.release()
        raise RuntimeError("Could not read initial frames from stream")

    prev_frame, prev_gray = preprocess_frame(frame1)
    curr_frame, curr_gray = preprocess_frame(frame2)

    last_alert_time = 0.0

    try:
        while True:
            frame_delta = cv2.absdiff(prev_gray, curr_gray)
            thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)

            contours, _ = cv2.findContours(
                thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )

            motion_detected = False
            display_frame = prev_frame.copy()

            for contour in contours:
                if cv2.contourArea(contour) < MIN_CONTOUR_AREA:
                    continue

                motion_detected = True
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(
                    display_frame,
                    (x, y),
                    (x + w, y + h),
                    (0, 255, 0),
                    2,
                )

            now = time.time()

            if motion_detected and (now - last_alert_time >= ALERT_COOLDOWN_SECONDS):
                snapshot_path = save_snapshots(display_frame)
                public_url = build_public_snapshot_url(snapshot_path)

                alert_text = f"Motion detected at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

                send_whatsapp_alert(alert_text, public_url)
                last_alert_time = now

            cv2.imshow("Motion Detector", display_frame)
            prev_frame, prev_gray = curr_frame, curr_gray

            ret, next_frame = cap.read()
            if not ret:
                break

            curr_frame, curr_gray = preprocess_frame(next_frame)

            if cv2.waitKey(1) == 27:
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

