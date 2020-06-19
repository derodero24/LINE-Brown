import os

from flask import Flask, abort, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (ImageMessage, MessageEvent, TextMessage,
                            TextSendMessage)

import reply

app = Flask(__name__)

# 環境変数取得
CHANNEL_ACCESS_TOKEN = os.environ['CHANNEL_ACCESS_TOKEN']
CHANNEL_SECRET = os.environ['CHANNEL_SECRET']

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


@app.route('/')
def index():
    return 'Hello World!'


@app.route('/callback', methods=['POST'])
def callback():
    ''' 毎回最初に実行 '''
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    print(f'Request body: {body}')

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    ''' テキストメッセージのとき '''
    message = event.message.text
    rep = reply.to_text_message(message)
    print(f'message: {message}\nreply: {rep}')

    # 送信
    if not rep == '':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=rep))


@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    '''画像のとき'''
    print('get image')
    id = event.message.id
    image = line_bot_api.get_message_content(id)
    data = reply.face_api(image.content)
    rep = reply.age_gender(data)
    print(f'reply: {rep}')

    # 送信
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=rep))


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000))
    )
