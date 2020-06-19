import base64
import json
import os

import requests

# 環境変数取得
TRANSLATION_URL = os.environ['TRANSLATION_URL']
CHAT_API_URL = os.environ['CHAT_API_URL']
CHAT_API_KEY = os.environ['CHAT_API_KEY']
FACEPP_URL = os.environ['FACEPP_URL']
FACEPP_API_KEY = os.environ['FACEPP_API_KEY']
FACEPP_API_SECRET = os.environ['FACEPP_API_SECRET']


def is_ascii(text):
    '''半角文字列の判定'''
    if not text:
        return False
    return all(ord(char) < 128 for char in text)


def tranlation(text):
    ''' 翻訳 '''
    reply = requests.get(
        url=TRANSLATION_URL,
        params={'text': text, 'source': 'en', 'target': 'ja'}
    ).text
    return reply


def chat(text):
    '''雑談'''
    params = {
        'key': CHAT_API_KEY,
        'message': text
    }
    reply = requests.get(CHAT_API_URL, params).json()
    print(reply)
    return reply['result']


def to_text_message(message):
    if is_ascii(message):  # 英語翻訳
        return tranlation(message)
    elif message:
        return chat(message)
    else:
        print('Error at to_text_message()')
        return


def face_api(image):
    '''FACE API'''
    data = {
        'api_key': FACEPP_API_KEY,
        'api_secret': FACEPP_API_SECRET,
        'image_base64': base64.b64encode(image),
        'return_attributes': 'age,gender'
    }
    res = requests.post(url=FACEPP_URL, data=data)
    content = res.content
    print(content)
    return content


def age_gender(data):
    '''年齢＆性別'''
    if data == b'[]':
        return 'お顔が見当たんないよ？'
    json_ = json.loads(data)
    face_info = json_['faces'][0]['attributes']
    print(face_info)
    gender_dic = {'Male': '男性', 'Female': '女性'}
    gender = gender_dic[face_info['gender']['value']]
    age = str(int(face_info['age']['value']))
    return age + '歳 ' + gender
