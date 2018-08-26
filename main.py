import os
import re

from flask import Flask, abort, request

# from urllib.parse import urlencode
#
# import requests
import reply
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# アプリ作成
app = Flask(__name__)

# 環境変数取得
CHANNEL_ACCESS_TOKEN = os.environ['CHANNEL_ACCESS_TOKEN']
CHANNEL_SECRET = os.environ['CHANNEL_SECRET']
# TRANSLATION_URL = os.environ['TRANSLATION_URL']
# CHAT_API_URL = os.environ['CHAT_API_URL']
# CHAT_API_KEY = os.environ['CHAT_API_KEY']

# api,handler作成
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


def is_ascii(str):
    '''半角文字列の判定'''
    boolean = False
    if str:
        boolean = max([ord(char) for char in str]) < 128
    if not boolean:
        boolean = re.search(r'[’]+', str) is not None
    return boolean


def get_image(message_id):
    url = 'https://trialbot-api.line.me/v1/bot/message/' + message_id + '/content'
    headers = {'Authorization': CHANNEL_ACCESS_TOKEN}
    requests.get(url, headers=headers)

# def tranlation(text):
#     '''翻訳'''
#     params = urlencode({
#         'text': text,
#         'source': 'en',
#         'target': 'ja'
#     })
#     url = TRANSLATION_URL + '?' + params
#     reply = requests.get(url).text
#     return reply
#
#
# def chat(text):
#     '''雑談'''
#     params = urlencode({
#         'key': CHAT_API_KEY,
#         'message': text
#     })
#     url = CHAT_API_URL + '?' + params
#     reply = requests.get(url).json()
#     return reply['result']


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

    type = event.message.type
    if type == 'text':  # テキスト
        text = event.message.text
        print('text :', text)
        if is_ascii(text):  # 英語翻訳
            rep = reply.tranlation(text)
            print('reply :', rep)
        elif text:
            rep = reply.chat(text)
            print('reply :', rep)
        else:
            print('例外')
            return

            # elif type == 'image':  # 画像
            #
            # else:  # その他
            #     print('例外')
            #     return

    # 送信
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=rep))


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
