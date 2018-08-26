import os
import re
from urllib.parse import urlencode

import requests

# import cv2

# 環境変数取得
FACE_API_URL = os.environ['FACE_API_URL']
FACE_API_KEY = os.environ['FACE_API_KEY']


def is_ascii(str):
    '''半角文字列の判定'''
    boolean = False
    if str:
        boolean = max([ord(char) for char in str]) < 128
    if not boolean:
        boolean = re.search(r'[’]+', str) is not None
    return boolean


def face_api(bynary):
    '''FACE API'''
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': FACE_API_KEY,
    }
    params = urlencode({
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender'
    })
    url = FACE_API_URL + '?' + params
    res = requests.post(url, data=bynary, headers=headers)
    return res.content


# def display_expression(data, bynary):
#     '''顔枠＆性別＆年齢'''
#     img = io.BytesIO(bynary)
#     img = cv2.imread(img)
#     json_ = json.loads(data)
#
#     font = cv2.FONT_HERSHEY_PLAIN
#     font_size = 1.5
#     for face in json_:
#         f_rec = face['faceRectangle']
#         width = f_rec['width']
#         height = f_rec['height']
#         left = f_rec['left']
#         top = f_rec['top']
#         cv2.rectangle(img, (left, top), (left + width,
#                                          top + height), (0, 200, 0), 2)
#
#         f_attr = face['faceAttributes']
#         gender = f_attr['gender']
#         age = int(f_attr['age'])
#         cv2.putText(img, gender + str(age), (left, 30 + top + height),
#                     font, font_size, (0, 200, 0), 2)
