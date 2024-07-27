# Written by Hamza Farahat <farahat.hamza1@gmail.com>, 7/27/2024
# Contact me for more information:
# Contact Us: https://terabyte-26.com/quick-links/
# Telegram: @hamza_farahat or https://t.me/hamza_farahat
# WhatsApp: +212772177012
import asyncio

from pyrogram import Client, filters, enums, idle
from bs4 import BeautifulSoup
from flask import Flask
from requests import Session, Response

from consts import Consts

import requests
import threading

from helpers import send_message

app: Flask = Flask(__name__)

bot: Client = Client(
    "Designs_Extractor",
    api_id=Consts.API_ID,
    api_hash=Consts.API_HASH,
    bot_token=Consts.BOT_TOKEN
)





@app.route('/')
def home():
    return 'Hello world !'


@bot.on_message(filters.command(['start']) & filters.private)
async def start(_, m):
    chat_id = m.chat.id
    await bot.send_chat_action(chat_id, enums.ChatAction.TYPING)

    await m.reply_text("Hello, send the listing URL, and let's work !!")


@bot.on_message(filters.text & filters.private)
async def extractor(c, m):
    message: str = str(m.text.strip())
    chat_id: int = m.chat.id

    await bot.send_chat_action(chat_id=chat_id, action=enums.ChatAction.PLAYING)

    session: Session = requests.Session()
    response: Response = session.get(message, headers=Consts.HEADERS)

    soup: BeautifulSoup = BeautifulSoup(response.content, 'html.parser')
    del response

    urls = str(soup).split("var obj = jQuery.parseJSON('")[1].split('"')
    del soup

    file_name = None

    for word in urls:
        if '._CLa%7C' in word:
            file_name = word.split('.png')[0].split('%7C')[-1]
            break

    design_url: str = Consts.AMAZON_URL + file_name + '.png'
    await c.send_photo(chat_id=chat_id, photo=design_url) if file_name else print('Error')


if __name__ == "__main__":

    bot.start()
    print("I'm live !!")
    threading.Thread(target=app.run, args=("0.0.0.0", 8080), daemon=True).start()

    send_message(Consts.OWNER_ID, "💬 [INFO] Starting The Bot")

    idle()
    bot.stop()

