import time
from hashlib import md5

s = "appkey=wxapp&latitude=23.0833100000&longitude=113.3172000000&nonce_str=pr8ac2eo1f8jd7e8bpczboge5b5lyfys&timestamp=1637836560"
sign = '24b1f78c6771a1563d66cdb4bfd048fb'

print(md5(s.encode()).hexdigest() == sign)