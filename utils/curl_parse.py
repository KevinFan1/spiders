import json
import re
from json import JSONDecodeError
import requests


class CURLParser:
    def __init__(self, curl_data: str):
        self.curl_data = curl_data
        self._parse()

    def _parse(self):
        pattern = r'curl \'(.+?)\' '
        _url = str(re.findall(pattern, self.curl_data)[0])
        self.url = _url

        uri_ret = _url.split('?')
        if len(uri_ret) == 1:
            self.uri = uri_ret[0]
            self.params = {}
        else:
            self.uri, _params_str = uri_ret
            self.params = {i.split('=')[0]: i.split('=')[1] for i in _params_str.split('&')}

    @property
    def headers(self):
        pattern = '-H.+?\'(.+?)\' '
        headers_str = re.findall(pattern, self.curl_data)

        _headers = {}
        for header in headers_str:
            k, v = re.findall(r'(.+): (.+)$', header)[0]
            _headers[k] = v

        return _headers

    @property
    def data(self):
        pattern = '--data-raw \'(.+?)\' '
        try:
            _data_str = re.findall(pattern, self.curl_data)[0]
            if 'json' in self.headers.get('content-type', self.headers.get('Content-Type')):
                return json.loads(_data_str)
            return _data_str
        except JSONDecodeError:
            return


if __name__ == '__main__':
    data = """curl 'https://www.bilibili.com/video/BV1Yb4y1t7jF?spm_id_from=333.851.b_7265706f7274466972737432.8' \
      -H 'authority: www.bilibili.com' \
      -H 'pragma: no-cache' \
      -H 'cache-control: no-cache' \
      -H 'sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"' \
      -H 'sec-ch-ua-mobile: ?0' \
      -H 'sec-ch-ua-platform: "macOS"' \
      -H 'upgrade-insecure-requests: 1' \
      -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36' \
      -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' \
      -H 'sec-fetch-site: same-origin' \
      -H 'sec-fetch-mode: navigate' \
      -H 'sec-fetch-user: ?1' \
      -H 'sec-fetch-dest: document' \
      -H 'referer: https://www.bilibili.com/' \
      -H 'accept-language: zh-CN,zh;q=0.9' \
      -H $'cookie: _uuid=FE8A7C39-10B0-018B-F41E-F2DFAA875AAE45369infoc; buvid3=21AB4796-EA6C-469B-824E-E45D1A131E8434765infoc; blackside_state=1; rpdid=|(k|k)~|)mYl0J\'uYu)Ylk~Rl; buvid_fp=21AB4796-EA6C-469B-824E-E45D1A131E8434765infoc; LIVE_BUVID=AUTO8016233073918521; PVID=1; fingerprint=72e324fc3ee8b81b613257c9362bbc59; buvid_fp_plain=63AAA4A3-3ECA-4F2C-962A-051FD219994634758infoc; SESSDATA=9d102a29%2C1643009593%2Cbaf4a%2A71; bili_jct=4d1f56c209518c1c576df4ea6e98cf4c; DedeUserID=14920973; DedeUserID__ckMd5=28138728127d3388; sid=55k1bj0i; CURRENT_QUALITY=80; CURRENT_FNVAL=976; video_page_version=v_old_home; b_lsid=798DEA108_17D6F1811E9; bsource=search_google; innersign=1' \
      --compressed"""
    parser = CURLParser(data)
    uri = parser.uri
    params = parser.params
    headers = parser.headers

    resp = requests.get(uri, params=params, headers=headers)
    print(resp.text)
