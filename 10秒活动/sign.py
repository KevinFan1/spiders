import json
import random
import time
from hashlib import md5
import requests


# raw = {
#     "user_time": 9971,
#     "timestamp": 1640746317,
#     "nonce": "6f8ba87cead96e58feb801fc073ff960",
#     "data": "user_time=9971",
#     "signature": "47b7bd97724e92dfd52427d9d5902ebe"
# }
class SecKill:
    def __init__(self):
        self.headers = {
            'origin': 'https://you.95118.cn',
            'appurl': '/a2/tools/nhab/20',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) MicroMessenger/6.8.0(0x16080000) MacWechat/3.2.2(0x13020210) NetType/WIFI WindowsWechat',
            'authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiI5NTExOC5jbiIsImF1ZCI6Ijk1MTE4LmNuIiwiZGF0YSI6eyJ1aWQiOjY1ODYzOX0sImlhdCI6MTY0MDgzNTA3OSwibmJmIjoxNjQwODM1MDc5LCJleHAiOjE2NDA4MzY4NzksImV4cGlyZSI6MTgwMH0.SAgPvT44tDsbNno_-gBA3v_S5HWY94kqnfvp-b8lL-utKl45Rv6wwQ8k2rpt5Xts3lPVLZW6lOZPUIskVavVvDyYRY8PkQ3dU1v9nvcNSIwbDsz7kWR3rhEGvNZnmknW8M9-WM-pFyfAgz-O5gtcO6UQHqu-9S6ds8A02nDAwT8'
        }
        self.y = 'Zgc3a7jNqANK2nbVBluSgxKKaXZs0A'

    def start(self):
        params = {}
        o = '&'.join([f'{k}={v}' for k, v in params.items()])
        a = int(time.time())
        s = md5((str(a) + self.y + str(random.random()) + str(random.random())).encode()).hexdigest()
        sign = md5((str(a) + s + o + self.y).encode()).hexdigest()
        params['timestamp'] = a
        params['nonce'] = s
        params['data'] = o
        params['signature'] = sign
        url = 'https://api.95118.cn/a/dz3/start'
        return requests.post(url, json=params, headers=self.headers, verify=False).json()

    def join(self):
        data = {
            "user_time": 10000,
        }
        o = '&'.join([f'{k}={v}' for k, v in data.items()])
        a = int(time.time())
        s = md5((str(a) + self.y + str(random.random()) + str(random.random())).encode()).hexdigest()
        sign = md5((str(a) + s + o + self.y).encode()).hexdigest()

        data['timestamp'] = a
        data['nonce'] = s
        data['data'] = o
        data['signature'] = sign
        url = 'https://api.95118.cn/a/dz3/join'
        resp = requests.post(url, json=data, headers=self.headers, verify=False)
        return resp.json()

    def run(self):
        print(self.start())
        time.sleep(10)
        print(self.join())


if __name__ == '__main__':
    SecKill().run()
