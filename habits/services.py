import requests

from Tracker_habits import settings


def send_message(
    chat_id,
    text,
):
    params = {
        "text": text,
        "chat_id": chat_id,
    }
    requests.get(
        f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage",
        params=params,
    )
