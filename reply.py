
from urllib.parse import urlencode

import requests


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
