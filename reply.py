import base64
import io
import json
import os

import requests
from PIL import Image, ImageDraw, ImageFont

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
    # url = CHAT_API_URL + '?' + params
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
    # headers = {
    #     'Content-Type': 'multipart/form-data'
    # }
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


def display_expression(data, image):
    '''顔枠＆性別＆年齢'''
    # print('from display_expression')
    image = io.BytesIO(image)
    # print('from display_expression')
    image = Image.open(image)
    d = ImageDraw.Draw(image)
    # image = cv2.imread(image)
    # print('from display_expression')
    json_ = json.loads(data)

    # font = cv2.FONT_HERSHEY_PLAIN
    # font_size = 1.5
    font = ImageFont.truetype(
        '/usr/share/fonts/vlgothic/VL-PGothic-Regular.ttf', 28)
    # print('from display_expression')
    for face in json_['faces']:
        # print(json.dumps(face))
        f_rec = face['face_rectangle']
        width = f_rec['width']
        height = f_rec['height']
        left = f_rec['left']
        top = f_rec['top']
        print(f'{width}, {height}, {left}, {top}')
        cord = [(left, top), (left + width, top + height)]
        d.rectangle(cord, outline='green', width=4)
        # cv2.rectangle(image, (left, top), (left + width,
        #                                    top + height), (0, 200, 0), 2)

        f_attr = face['attributes']
        gender = f_attr['gender']['value']
        age = f_attr['age']['value']
        d.text((left + (width // 2), top - 30), gender + str(age),
               fill='green', font=font, align='center')
        # cv2.putText(image, gender + str(age), (left, 30 + top + height),
        #             font, font_size, (0, 200, 0), 2)
        # print(f'{width}, {height}, {left}, {top}')

    # cv2.imwrite('test.png', image)
    image.save('test.png')
