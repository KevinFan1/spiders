import base64
import json
import httpx
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

iv = '1oZNRqwWnlbmajnU'
key = 'MV7EahKPr2w0bwKH'
mode = AES.MODE_CBC


def decrypt(enc):
    enc = base64.b64decode(enc)
    cipher = AES.new(key.encode(), mode, iv.encode())
    return cipher.decrypt(enc).decode().strip().replace('', '')


def encrypt(data: dict):
    encrypt_str = pad(json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode(), 16)
    cipher = AES.new(key.encode(), mode, iv.encode())
    return base64.b64encode(cipher.encrypt(encrypt_str)).decode()


if __name__ == '__main__':
    url = 'https://apptransfer.gzhotelgroup.com/man-api/api/wxhotel/hotel/getHotelList'
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E217 MicroMessenger/6.8.0(0x16080000) NetType/WIFI Language/en Branch/Br_trunk MiniProgramEnv/Mac'
    }
    post_data = {"cityId": "", "name": "", "orderBys": [{"columnName": "", "dir": 0}], "page": 1, "pageSize": 10,
                 "search": ""}
    post_str = encrypt(post_data)

    resp = httpx.post(url, json=post_str, headers=headers).json()
    # for k, v in resp.items():
    #     print(k)
    #     print(decrypt(v))
    #     print('==' * 50)

    data = json.loads(decrypt(resp['data']))

    total = data['total']
    pages = data['pages']
    for record in data['records']:
        print(record)
