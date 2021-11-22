import json
import requests
from system import Configurator
from linebot.models import (MessageEvent)


class Requester:

    def __init__(self, config: Configurator):
        self.configurator = config
    
    def post_dialogflow(self, request):
        url = self.configurator.get('dialogflow.webhook')
        headers = dict()
        for key,value in request.headers.items():
            headers[key] = value
        headers['Host'] = self.configurator.get('dialogflow.host')
        response = requests.post(url, data = json.dumps(request.json), headers=headers)

    def post_user(self, event, display_name):
        user_id = event.source.user_id
        url = self.configurator.get('api.user')
        headers = { 'Content-Type': 'application/json'}
        payload = {
            'replyToken': event.reply_token,
            'source': { 'type': 'user', 'user_id': user_id},
            'display_name': display_name
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        return response

    def get_user(self, user_id):
        url = self.configurator.get('api.user')+'?user_id=' + user_id
        response = requests.get(url)
        return response

    def update_user(self, data):
        print('data')
        print(data)
        user_id = data['user_id']
        print('update_user response')
        url = self.configurator.get('api.user')+'?user_id=' + user_id
        response = requests.put(url, data=json.dumps(data))
        print(response.json)
        return response.json

    def delete_user(self, user_id):
        url = self.configurator.get('api.user')+'?user_id=' + user_id
        response = requests.delete(url)
        return response