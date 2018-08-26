import os
from io import BytesIO

from flask import Flask, abort, request

import reply
import tools
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageMessage

# アプリ作成
app = Flask(__name__)

# 環境変数取得
CHANNEL_ACCESS_TOKEN = os.environ['CHANNEL_ACCESS_TOKEN']
CHANNEL_SECRET = os.environ['CHANNEL_SECRET']

# api,handler作成
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


# def get_image(message_id):
#     '''画像取得'''
#     url = 'https://trialbot-api.line.me/v1/bot/message/' + message_id + '/content'
#     headers = {'Authorization': CHANNEL_ACCESS_TOKEN}
#     requests.get(url, headers=headers)


@app.route("/callback", methods=['POST'])
def callback():
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
    if tools.is_ascii(text):  # 英語翻訳
        rep = reply.tranlation(text)
        print('reply :', rep)
    elif text:
        rep = reply.chat(text)
        print('reply :', rep)
    else:
        print('例外')
        return

    # 送信
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=rep))


@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    '''画像のとき'''
    message_id = event.message.id
    message_content = line_bot_api.get_message_content(message_id)

    image = BytesIO(message_content.content)
    print('got it')


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
