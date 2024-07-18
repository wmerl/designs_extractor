from pyrogram import Client, filters, enums, idle
from bs4 import BeautifulSoup
from flask import Flask

import requests
import threading

app = Flask(__name__)

bot = Client("Yplatinum", api_id=20782961, api_hash="c68f73d3dc4c383a155cb167426c68d4", bot_token="6244633840:AAGKdF_SBD3DjYEEx0n5EEzyTFntcb9QOfQ")
amazon_url = "https://m.media-amazon.com/images/I/"
session = requests.Session()

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-encoding': 'gzip, deflate, br',
    'cookie': 'csm-sid=741-6601084-4447612; x-amz-captcha-1=1692018940893386; x-amz-captcha-2=f6dSjiH0R2Jmju2q0h+7UQ==; session-id=141-0886133-7126549; session-id-time=2082787201l; i18n-prefs=USD; sp-cdn="L5Z9:MA"; ubid-main=135-2487945-7796461; lc-main=en_US; session-token=qa1dMvnYCyrrn8mrjcQ5hau3cSNEbesc9Syc90NIBldFgN1qVIULPTDuDFPxAxog1joPIf/eoXiLH9kw0kri1l0XrBeq+a8j4GbFm53J/hndKnLc0+avRmJ4muzs3/ocbY2jkfEzHpr0EaumjFsmc4U2VwVok76snhoAXC4D7PTq3vDz/XL4k7BVrbshaWEXno5WvYAPcHxnfamf5mog4jciFpIAqNrpxxXQqKhRCeM=; csm-hit=tb:HBRP7X7XR0RYCQD4QWGJ+b-B0104TEVFQAYJ78JX5MZ|1692131402404&t:1692131402404&adb:adblk_no',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
}


@app.route('/')
def home():
    return 'Hello world !'


@bot.on_message(filters.command(['start']) & filters.private)
async def start(c, m):
    chat_id = m.chat.id
    await bot.send_chat_action(chat_id, enums.ChatAction.TYPING)

    await m.reply_text("Hello, send the listing URL, and let's work !!")


@bot.on_message(filters.text & filters.private)
async def extractor(c, m):
    message = str(m.text.strip())
    chat_id = m.chat.id

    response = session.get(message, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    urls = str(soup).split("var obj = jQuery.parseJSON('")[1].split('"')
    file_name = None

    for word in urls:
        if '._CLa%7C' in word:
            file_name = word.split('.png')[0].split('%7C')[-1]
            break

    await c.send_photo(chat_id, amazon_url + file_name + '.png') if file_name else print('Error')


if __name__ == "__main__":
    bot.start()
    print("I'm live !!")
    threading.Thread(target=app.run, args=("0.0.0.0", 8080), daemon=True).start()
    idle()
    bot.stop()

