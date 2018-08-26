
import os
from urllib.parse import urlencode

import requests

# 環境変数取得
TRANSLATION_URL = os.environ['TRANSLATION_URL']
CHAT_API_URL = os.environ['CHAT_API_URL']
CHAT_API_KEY = os.environ['CHAT_API_KEY']


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
