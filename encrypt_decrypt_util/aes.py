# -*- coding: utf-8 -*-

import base64
from Crypto.Cipher import AES
from urllib.parse import quote, unquote

from utils.wrapper_util.wrappers import warning

"""AES加解密"""


def encrypt(aes_key, data, mode=AES.MODE_CBC):
    """加密"""
    key = base64.b64decode(aes_key)
    cipher = AES.new(key, mode=mode)
    bs = AES.block_size
    pad = lambda s: s + (bs - len(s) % bs) * chr(bs - len(s) % bs)
    if not isinstance(data, str):
        data = str(data)
    payload = pad(quote(data.encode())).encode()
    cipher_text = escape_symbol(base64.b64encode(cipher.encrypt(payload)).decode())
    return cipher_text


def decrypt(aes_key, data, mode=AES.MODE_CBC):
    """解密"""
    key = base64.b64decode(aes_key)
    cipher = AES.new(key, mode=mode)
    decrypt_text = cipher.decrypt(base64.b64decode(restore_symbol(data)))
    unpad = lambda s: s[0:-ord(s[-1])]
    cipher_text = unquote(unpad(decrypt_text.decode()))

    return cipher_text


def escape_symbol(content):
    if content.find("+") > 0 or content.find("/") > 0:
        content = content.replace("+", ".")
        content = content.replace("/", "_")
    return content


def restore_symbol(content):
    if content.find(".") > 0 or content.find("_") > 0:
        content = content.replace(".", "+")
        content = content.replace("_", "/")
    return content


@warning()
def encrypt_key(data, mode=AES.MODE_CBC):
    # 生成加密密钥
    # 密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用

    cipher = AES.new(data.encode("utf-8"), mode=mode)
    bs = AES.block_size
    pad = lambda s: s + (bs - len(s) % bs) * chr(bs - len(s) % bs)
    payload = pad(quote(data.encode())).encode()
    cipher_text = base64.b64encode(cipher.encrypt(payload)).decode()
    return cipher_text


if __name__ == '__main__':
    data = 0
    key = encrypt_key("315ccddc9e04407abf5c3f87c67f506e")
    print(f"encrypt_key: {key}")




