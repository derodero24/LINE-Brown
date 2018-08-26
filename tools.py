
import re


def is_ascii(str):
    '''半角文字列の判定'''
    boolean = False
    if str:
        boolean = max([ord(char) for char in str]) < 128
    if not boolean:
        boolean = re.search(r'[’]+', str) is not None
    return boolean
