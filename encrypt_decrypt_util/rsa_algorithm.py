# -*- coding: utf-8 -*-


import base64
import json
from binascii import a2b_base64

from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature.PKCS1_v1_5 import new
from Crypto.Util.asn1 import DerSequence


# 加密
def encrypt(data, pub_key_path, default_length=117):
    """
    单次加密串的长度最大为 (key_size/8)-11
    1024bit的证书用100， 2048bit的证书用 200
    """

    with open(pub_key_path, "r") as f:
        key = f.read()
        # Convert from PEM to DER
        lines = key.replace(" ", '').split()
        der = a2b_base64(''.join(lines[1:-1]))

        # Extract subjectPublicKeyInfo field from X.509 certificate (see RFC3280)
        cert = DerSequence()
        cert.decode(der)
        tbsCertificate = DerSequence()
        tbsCertificate.decode(cert[0])
        subjectPublicKeyInfo = tbsCertificate[6]

        # Initialize RSA key
        rsa_key = RSA.importKey(subjectPublicKeyInfo)
        cipher = Cipher_pkcs1_v1_5.new(rsa_key)
        data = data.encode()
        length = len(data)
        if length < default_length:
            cipher_text = base64.b64encode(cipher.encrypt(data)).decode()
            return cipher_text

        res = []
        offset = 0
        while length - offset > 0:
            if length - offset > default_length:
                res.append(cipher.encrypt(data[offset:offset + default_length]))
            else:
                res.append(cipher.encrypt(data[offset:]))
            offset += default_length
        cipher_text = b""
        for r in res:
            cipher_text += r
        cipher_text = base64.b64encode(cipher_text).decode()
        return cipher_text


# 解密
def decrypt(data, pri_key_path, default_length=128):
    """
    1024bit的证书用128，2048bit证书用256位
    """

    with open(pri_key_path) as f:
        key = f.read()
        rsa_key = RSA.importKey(key)
        cipher = Cipher_pkcs1_v1_5.new(rsa_key)
        data = base64.b64decode(data.encode())
        length = len(data)
        if length < default_length:
            decrypt_text = cipher.decrypt(data, b"ERROR")
            return decrypt_text
        res = []
        offset = 0
        while length - offset > 0:
            if length - offset > default_length:
                res.append(cipher.decrypt(data[offset:offset + default_length], b"ERROR"))

            else:
                res.append(cipher.decrypt(data[offset:], b"ERROR"))
            offset += default_length
        cipher_text = b""
        for r in res:
            cipher_text += r
        try:
            decrypt_text = json.loads(cipher_text.decode())
        except Exception as e:
            decrypt_text = cipher_text.decode()
        return str(decrypt_text) if type(decrypt_text) == int else decrypt_text


# 签名
def generate_signature(data, pri_key_path):
    with open(pri_key_path) as f:
        key = f.read()
        rsa_key = RSA.importKey(key)
        signer = new(rsa_key)
        digest = SHA.new()
        digest.update(base64.b64decode(data))
        sign = signer.sign(digest)
        signature = base64.b64encode(sign).decode()
        return signature


# 验签
def verify_signature(result, pub_key_path):
    sign = result.get("sign").encode()
    data = result.get("data").encode()
    with open(pub_key_path) as f:
        key = f.read()
        # Convert from PEM to DER
        lines = key.replace(" ", '').split()
        der = a2b_base64(''.join(lines[1:-1]))

        # Extract subjectPublicKeyInfo field from X.509 certificate (see RFC3280)
        cert = DerSequence()
        cert.decode(der)
        tbsCertificate = DerSequence()
        tbsCertificate.decode(cert[0])
        subjectPublicKeyInfo = tbsCertificate[6]

        rsa_key = RSA.importKey(subjectPublicKeyInfo)
        verifier = new(rsa_key)
        digest = SHA.new()
        # Assumes the data is base64 encoded to begin with
        digest.update(base64.b64decode(data))
        is_verify = verifier.verify(digest, base64.b64decode(sign))
        return is_verify


# 签名、加密结果
def generate_signature_and_encrypt(data, pri_key_path, pub_key_path):
    try:
        curr_ency = encrypt(data, pub_key_path)
    except Exception as e:
        return False, "签名失败！"

    try:
        curr_sign = generate_signature(curr_ency, pri_key_path)
    except Exception as e:
        return False, "加密失败！"

    return True, {"data": curr_ency, "sign": curr_sign}


# 验签、解密结果
def verify_signature_and_decrypt(data, pri_key_path, pub_key_path):
    verify_sign = verify_signature(data, pub_key_path)
    if verify_sign:
        try:
            decrypt_data = decrypt(data.get("data"), pri_key_path)
            return True, decrypt_data
        except Exception as e:
            return False, "解密失败！"
    else:
        return False, "验签失败！"


# 公钥解密(Crypto)
def decrypt_rsa(decrypt_key_file, cipher_text):
    key = open(decrypt_key_file, "rb").read()
    rsakey = RSA.importKey(key)
    raw_cipher_data = base64.b64decode(cipher_text)
    decrypted = rsakey.encrypt(raw_cipher_data, 0)[0]
    decrypted = decrypted[decrypted.index(b'\x00') + 1:]
    return decrypted.decode('utf-8')
