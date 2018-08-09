import requests
import json


class SmsYunPian(object):

    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_mess(self, code, mobile):
        params = {
            "apikey": self.api_key,
            "mobile": mobile,
            "text": "【罗新月的食品超市】您的验证码是：{code}。如非本人，请忽略本短信".format(code=code)
        }
        response = requests.post(self.single_send_url, params)
        # 可以在云片API里面看到返回回来的是JSON字符串，包括{
        #     "code": 0,
        #     "msg": "发送成功",
        #     "count": 1,
        #     "fee": 0.05,
        #     "unit": "RMB",
        #     "mobile": "13200000000",
        #     "sid": 3310228982
        # }
        data = json.loads(response.text)
        return data


# a9a17141c5b1c8555006f51f96896ce7
if __name__ == "__main__":
    yun_pian = SmsYunPian("a9a17141c5b1c8555006f51f96896ce7")
    yun_pian.send_mess("9543", "18281907652")