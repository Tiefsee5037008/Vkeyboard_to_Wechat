import json
import requests
myurl = 'https://api.vvhan.com/api/fy?text='


def Main(q):
    res = requests.post(url=myurl + q)
    res_dict = json.loads(res.text)
    return res_dict['data']['fanyi']


if __name__ == '__main__':
    print(Main('hello world'))
