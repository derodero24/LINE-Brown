import os
from io import BytesIO

from flask import Flask, abort, request

import reply
import tools
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (ImageMessage, MessageEvent, TextMessage,
                            TextSendMessage)

# アプリ作成
app = Flask(__name__)

# 環境変数取得
CHANNEL_ACCESS_TOKEN = os.environ['CHANNEL_ACCESS_TOKEN']
CHANNEL_SECRET = os.environ['CHANNEL_SECRET']

# api,handler作成
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


@app.route("/callback", methods=['POST'])
def callback():
    '''毎回最初に実行'''
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print(body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    '''テキストメッセージのとき'''
    text = event.message.text
    print('text :', text)
    rep = ''
    if tools.is_ascii(text):  # 英語翻訳
        rep = reply.tranlation(text)
    elif text:
        rep = reply.chat(text)
    else:
        print('例外')
        return

    print('reply :', rep)

    # 送信
    if not rep == '':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=rep))


@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    '''画像のとき'''
    id = event.message.id
    image = line_bot_api.get_message_content(id)
    data = tools.face_api(image.content)
    rep = reply.age_gender(data)

    # 送信
    if not rep == '':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=rep))


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
