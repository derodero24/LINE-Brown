import os
import re
from urllib.parse import urlencode

import requests
from flask import Flask, abort, request

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# アプリ作成
app = Flask(__name__)

# 環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ['YOUR_CHANNEL_ACCESS_TOKEN']
YOUR_CHANNEL_SECRET = os.environ['YOUR_CHANNEL_SECRET']
TRANSLATION_URL = os.environ['TRANSLATION_URL']
CHAT_API_URL = os.environ['CHAT_API_URL']
CHAT_API_KEY = os.environ['CHAT_API_KEY']

# api,handler作成
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


def is_ascii(str):
    '''半角文字列の判定'''
    boolean = False
    if str:
        boolean = max([ord(char) for char in str]) < 128
    if not boolean:
        boolean = re.search(r'[’]+', str) is not None
    return boolean


def tranlation(text):
    '''翻訳'''
    params = urlencode({
        'text': text,
        'source': 'en',
        'target': 'ja'
    })
    url = TRANSLATION_URL + '?' + params
    reply = requests.get(url).text
    return reply


def chat(text):
    '''雑談'''
    params = urlencode({
        'key': CHAT_API_KEY,
        'message': text
    })
    url = CHAT_API_URL + '?' + params
    reply = requests.get(url).json()
    return reply['result']


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    '''返信'''
    print(event)
    text = event.message.text
    print('text :', text)

    if is_ascii(text):  # 英語翻訳
        reply = tranlation(text)
        print('reply :', reply)
    elif text:
        reply = chat(text)
        print('reply :', reply)
    else:
        print('例外')
        return

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply))


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
