import random
from hashlib import md5
import time
from typing import Union

import httpx


def get_nonce_str(length=32):
    _chose_map = 'abcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join([random.choice(_chose_map) for i in range(length)])


def gen_sign_without_nonce_str(time_stamp: Union[int, str]):
    secret = '4c85e432n4n0z9fjdl00'
    encode_str = (str(time_stamp) + secret).encode()
    return md5(encode_str).hexdigest()


def get_sign_with_nonce_str(data: dict):
    _app_secrect_map = {
        'xcx001': "tRDlNb7cEidB2EC3",
        'wxxcx': "ADCK465JGdfs5KlaYq1",
        'wxapp': "8werw8fw23fLR98",
        'zbxcxzs': "4c89iur73kj499fjdle4",
        'user001': "od8rbcvohfkhzrs1",
        'life': "lhjngKj9lGHJi0ik",
        'wxpark': "x1WXbk10vb6fghjK"
    }
    if data.get('appkey') not in _app_secrect_map:
        raise ValueError('this appkey does not in mapping')

    keys = list(data.keys())
    keys.sort()
    enc_str = '&'.join(['{k}={v}'.format(k=key, v=data[key]) for key in keys])
    fir_md5 = md5(enc_str.encode()).hexdigest()
    sec_enc_str = fir_md5 + data['nonce_str'] + str(data['timestamp']) + _app_secrect_map[data['appkey']]
    return md5(sec_enc_str.encode()).hexdigest().upper()


url = 'https://wxapp.ruyigou.com/api/shopList'

cur_time = int(time.time())
post_data = {
    "appkey": "zbxcxzs",
    "nonce_str": get_nonce_str(),
    "timestamp": cur_time,
}
sign = get_sign_with_nonce_str(post_data)
post_data['sign'] = sign
headers = {
    'Host': 'wxapp.ruyigou.com',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E217 MicroMessenger/6.8.0(0x16080000) NetType/WIFI Language/en Branch/Br_trunk MiniProgramEnv/Mac',
    'Referer': 'https://servicewechat.com/wx0ae5e7e4b7ffd8ba/190/page-frame.html',
    'Accept-Language': 'zh-cn'
}
resp = httpx.post(url, json=post_data, headers=headers, verify=False)
print(resp.json())
