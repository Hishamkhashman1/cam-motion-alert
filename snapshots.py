import cv2
from datetime import datetime
from pathlib import Path

from config import SNAPSHOT_BASE_URL
from config import SNAPSHOT_DIR

SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)


def save_snapshots(frame) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    snapshot_path = SNAPSHOT_DIR / f"motion_{timestamp}.jpg"
    cv2.imwrite(str(snapshot_path), frame)
    return snapshot_path


def build_public_snapshot_url(snapshot_path: Path) -> str | None:
    if not SNAPSHOT_BASE_URL:
        return None

    return f"{SNAPSHOT_BASE_URL.rstrip('/')}/{snapshot_path.name}"
