import httpx

from utils.curl_parse import CURLParser
import requests

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

parse = CURLParser(data)

# resp = httpx.get(parse.uri,params=parse.params,headers=parse.headers)
# print(resp.text)
# print(parse.uri)
# print(parse.params)
# print(parse.headers)
url = "https://cn-gddg-dx-bcache-10.bilivideo.com/upgcxcode/89/35/440993589/440993589_ex1-1-30080.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1638256014&gen=playurlv2&os=bcache&oi=1903674070&trid=0000f8b90ca5a151431ab9b363fff9c7e2aeu&platform=pc&upsig=c5876e61d9fb2e5b42f2769df31c34ff&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,platform&cdnid=61310&mid=14920973&bvc=vod&nettype=0&codecexp=true&orderid=0,3&agrr=1&bw=331446&logo=80000000"

with open('a.mp4','wb') as f:
    f.write(httpx.get(url, headers=parse.headers).content)
