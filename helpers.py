# Written by Hamza Farahat <farahat.hamza1@gmail.com>, 7/27/2024
# Contact me for more information:
# Contact Us: https://terabyte-26.com/quick-links/
# Telegram: @hamza_farahat or https://t.me/hamza_farahat
# WhatsApp: +212772177012
import requests

from consts import Consts


def send_message(chat_id, text, silent=False):
    try:
        method: str = "sendMessage"
        url: str = f"https://api.telegram.org/bot{Consts.BOT_TOKEN}/{method}"

        data: dict[str: str] = {
            "chat_id": int(chat_id),
            "text": text,
            "parse_mode": "HTML",
            "disable_notification": silent,
        }

        resp = requests.post(url, data=data, timeout=3)
        if resp.json()["ok"] is False:
            print(resp.json())
        return resp
    except BaseException:
        pass