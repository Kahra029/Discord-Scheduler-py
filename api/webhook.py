import json
import requests

class Webhook():
    def __init__(self, body = None):
        with open('config.json', 'r') as f:
            config = json.load(f)
        self.__url = config['discord'].get('webhook')

    @property
    def body(self):
        return self.__body

    @body.setter
    def body(self, val):
        self.__body = val

    @property
    def url(self):
        return self.__url

    def send(self, body):
        requests.post(self.url,json.dumps(body),headers={'Content-Type': 'application/json'})