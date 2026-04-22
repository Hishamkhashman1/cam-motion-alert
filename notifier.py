import mimetypes
import urllib.request
from pathlib import Path

from config import NTFY_PRIORITY
from config import NTFY_SEND_SCREENSHOT
from config import NTFY_SERVER_URL
from config import NTFY_TAGS
from config import NTFY_TIMEOUT_SECONDS
from config import NTFY_TITLE
from config import NTFY_TOKEN
from config import NTFY_TOPIC


def _topic_url() -> str:
    return f"{NTFY_SERVER_URL.rstrip('/')}/{NTFY_TOPIC.lstrip('/')}"


def _common_headers(
    *,
    title: str,
    priority: int,
    tags: tuple[str, ...],
) -> dict[str, str]:
    headers = {
        "Title": title,
        "Priority": str(priority),
    }

    if tags:
        headers["Tags"] = ",".join(tags)

    if NTFY_TOKEN:
        headers["Authorization"] = f"Bearer {NTFY_TOKEN}"

    return headers


def _publish(
    *,
    body: bytes,
    content_type: str,
    headers: dict[str, str],
) -> None:
    request = urllib.request.Request(
        _topic_url(),
        data=body,
        method="POST",
    )
    request.add_header("Content-Type", content_type)

    for key, value in headers.items():
        request.add_header(key, value)

    with urllib.request.urlopen(request, timeout=NTFY_TIMEOUT_SECONDS):
        pass


def _publish_text(
    message: str,
    *,
    title: str,
    priority: int = NTFY_PRIORITY,
    tags: tuple[str, ...] = NTFY_TAGS,
    attach_url: str | None = None,
) -> None:
    headers = _common_headers(title=title, priority=priority, tags=tags)
    if attach_url:
        headers["Attach"] = attach_url

    _publish(
        body=message.encode("utf-8"),
        content_type="text/plain; charset=utf-8",
        headers=headers,
    )


def _publish_snapshot(
    snapshot_path: Path,
    *,
    title: str,
    priority: int = NTFY_PRIORITY,
    tags: tuple[str, ...] = NTFY_TAGS,
) -> None:
    headers = _common_headers(title=title, priority=priority, tags=tags)
    headers["Filename"] = snapshot_path.name

    content_type = mimetypes.guess_type(snapshot_path.name)[0] or "application/octet-stream"

    _publish(
        body=snapshot_path.read_bytes(),
        content_type=content_type,
        headers=headers,
    )


def send_motion_alert(
    body: str,
    snapshot_path: Path | None = None,
    snapshot_url: str | None = None,
) -> None:
    if NTFY_SEND_SCREENSHOT and snapshot_path:
        if snapshot_url:
            _publish_text(
                body,
                title=NTFY_TITLE,
                attach_url=snapshot_url,
            )
            print(f"[INFO] ntfy sent with snapshot URL: {snapshot_url}")
            return

        _publish_snapshot(snapshot_path, title=f"{NTFY_TITLE}: {body}")
        print(f"[INFO] ntfy sent with local snapshot: {snapshot_path.name}")
        return

    _publish_text(body, title=NTFY_TITLE)
    print(f"[INFO] ntfy sent to {NTFY_TOPIC}")
