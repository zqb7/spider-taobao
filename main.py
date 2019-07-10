import requests
import json
from common.util import Cookie, generate_js, JServer, generate_params
"""
主要参数是_m_h5_tk
sign生成的主要条件是：时间戳+token+页码数------别的已经固定了
"""
HEADER = {
    "Host": "h5api.m.taobao.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0",
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://2.taobao.com/",
    "Connection": "keep-alive",
    "Cookie": "",
    "TE": "Trailers"
}


class Spider(object):
    """爬取闲鱼"""
    def __init__(self):
        self.req = requests.Session()
        self.cookie = Cookie()
        self.token = self.cookie.token
        HEADER["Cookie"] = self.cookie.cookie
        self.req.headers.update(HEADER)

    def run(self, page_number):
        js, timestamp = generate_js(page_number, self.token)
        res = self.req.get("https://h5api.m.taobao.com/h5/mtop.taobao.idle.home.nextfresh/3.0/",
                           timeout=10,
                           headers=HEADER,
                           params=generate_params(timestamp, JServer().get(js)["message"], page_number))
        try:
            json_str = res.text.strip().rstrip(")").lstrip("mtopjsonp5(")
            json_data = json.loads(json_str, strict=False)
            if json_data['ret'][0] == "SUCCESS::调用成功":
                print(json_data)
                self.save(json_data)
                if json_data['data']['nextPage'] == "true":
                    return True
            elif json_data['ret'][0] == "FAIL_SYS_TOKEN_EMPTY::令牌为空":
                print("是否忘记传入cookie?")
                exit(1)
            elif json_data['ret'][0] == "FAIL_SYS_ILLEGAL_ACCESS::非法请求":
                print("FAIL_SYS_ILLEGAL_ACCESS::非法请求")
        except Exception as e:
            print(e)

    @staticmethod
    def save(data):
        with open("data.json", 'a+', encoding='utf-8') as f:
            f.write(str(data) + '\n')


if __name__ == '__main__':
    spider = Spider()
    num = 1
    while True:
        flag = spider.run(num)
        if flag:
            num += 1
            continue
        else:
            break

