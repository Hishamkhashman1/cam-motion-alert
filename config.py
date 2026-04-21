import os
from pathlib import Path

from dotenv import load_dotenv

"""TODO: Load `.env` values and define all shared configuration constants for the motion alert app."""
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

# TODO: Read RTSP_URL and Twilio credentials from the environment.
RTSP_URL = os.getenv("RTSP_URL")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM")
TWILIO_WHATSAPP_TO = os.getenv("TWILIO_WHATSAPP_TO")
SNAPSHOT_BASE_URL = os.getenv("SNAPSHOT_BASE_URL")


# TODO: Define SNAPSHOT_BASE_URL, SNAPSHOT_DIR, MIN_CONTOUR_AREA, ALERT_COOLDOWN_SECONDS, and FRAME_WIDTH.
SNAPSHOT_DIR = BASE_DIR / "snapshots"
# TODO: Validate required settings and raise a clear error when they are missing.
