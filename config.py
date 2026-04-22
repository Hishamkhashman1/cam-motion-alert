import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

RTSP_URL = os.getenv("RTSP_URL")
NTFY_SERVER_URL = os.getenv("NTFY_SERVER_URL", "https://ntfy.sh")
NTFY_TOPIC = os.getenv("NTFY_TOPIC")
NTFY_TITLE = os.getenv("NTFY_TITLE", "Camera Alert")
NTFY_PRIORITY = int(os.getenv("NTFY_PRIORITY", "4"))
NTFY_TAGS = tuple(
    tag.strip() for tag in os.getenv("NTFY_TAGS", "").split(",") if tag.strip()
)
NTFY_TIMEOUT_SECONDS = float(os.getenv("NTFY_TIMEOUT_SECONDS", "10"))
NTFY_SEND_SCREENSHOT = os.getenv("NTFY_SEND_SCREENSHOT", "0").lower() in {
    "1",
    "true",
    "yes",
    "on",
}
NTFY_TOKEN = os.getenv("NTFY_TOKEN")
SNAPSHOT_BASE_URL = os.getenv("SNAPSHOT_BASE_URL")

SNAPSHOT_DIR = BASE_DIR / "snapshots"
MIN_CONTOUR_AREA = 2500
ALERT_COOLDOWN_SECONDS = 30
FRAME_WIDTH = 960

if not RTSP_URL:
    raise RuntimeError("RTSP_URL is missing in .env")

if not NTFY_TOPIC:
    raise RuntimeError("NTFY_TOPIC is missing in .env")
