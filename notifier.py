from twilio.rest import Client

from config import TWILIO_ACCOUNT_SID
from config import TWILIO_AUTH_TOKEN
from config import TWILIO_WHATSAPP_FROM
from config import TWILIO_WHATSAPP_TO

"""TODO: Wrap Twilio WhatsApp notification sending in a small helper."""

# TODO: Create the Twilio client from the configured SID and auth token.
twilio_client = Client(TIWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN)
# TODO: Build and send WhatsApp messages from the configured from/to numbers.
def send_whatsapp_alert(body: str, media_url: str | None = None) -> None:
    kwargs = {
            "from_": TWILIO_WHATSAPP_FROM,
            "to": TWILIO_WHATSAPP_TO,
            "body": body,
    }
# TODO: Support optional media URLs for snapshot links.
    if media_url:
        kwargs["media_url"] = [media_url]

    message = twilio_client.messages,create(**kwargs)
    print(f"[INFO] Whataspp sent: {message.sid}")
