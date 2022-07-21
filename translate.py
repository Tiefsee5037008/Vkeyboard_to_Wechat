# /usr/bin/env python
# coding=utf8

import json
import http.client  # 修改引用的模块
import hashlib  # 修改引用的模块
from urllib import parse
import random

appid = '20220721001278990'  # 你的appid
secretKey = 'CIlw7W_yYyBQwBA81Ljv'  # 你的密钥


def Main(text, fromLang='en', toLang='zh'):
    myurl = '/api/trans/vip/translate'
    salt = random.randint(32768, 65536)
    httpClient = None
    sign = appid + text + str(salt) + secretKey
    m1 = hashlib.md5()
    m1.update(sign.encode("utf-8"))
    sign = m1.hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + parse.quote(text) + '&from=' + \
        fromLang + '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign

    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        response = httpClient.getresponse()

        # 转码
        html = response.read().decode('utf-8')
        html = json.loads(html)
        dst = html["trans_result"][0]["dst"]
        print('\n 译文：', dst)
        return dst
    except Exception as e:
        print(e)
        return 'Translate Error'
    finally:
        if httpClient:
            httpClient.close()


if __name__ == '__main__':
    Main('What is the weather today?')
