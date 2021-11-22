import json, requests
from system import Configurator
from linebot import LineBotApi
from linebot.exceptions import LineBotApiError
configurator = Configurator("private/config.json")
line_bot_api = LineBotApi(configurator.get('line.access_token'))

class LineResponse:

    def __init__(self, access_token: str):
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer 7FWV4LbCf8J0cJD0xspMHiqCAHmTbHC2Wn/kd2xWfr2GcxDL/u8AhRyVFdWDFhXMTYfFJSWw000X5KTvER/Z+k/y0DXm4sk2Y5JmlSFND+EmFYUPkqDTcUXwimXcaZl1lE3o2ip0FDlCJ2DIGGojUAdB04t89/1O/w1cDnyilFU='.format(access_token)
        }

    def push(self, data): 
        url = 'https://api.line.me/v2/bot/message/push'
        response = requests.post(url, data = data, headers=self.headers)
    
    def get_profile(self, userId):
        try:
            profile = line_bot_api.get_profile(userId)
            return profile
        except LineBotApiError as e:
            print(e.error)
