import  json
import datetime
import random
from api.calendarApi import CalendarApi
from data.calendarData import CalendarData
from api.webhook import Webhook
from data.webhookData import WebhookData
from data.webhookData import WebhookContent

class SchedulerLogic():
    def __init__(self):
        with open('config.json', 'r') as f:
            config = json.load(f)
            self.__config = config
        
    @property
    def config(self):
        return self.__config

    def getEvent(self):
        try:
            calData = CalendarData()
            calendar = CalendarApi()
            result = calendar.get(day=0, routine=True)

            webhook = Webhook()
            webhookData = WebhookData()
            webhookContent = WebhookContent()

            if result != []:
                message = self.config["webhook"].get('message').get('event_message')
                body = webhookContent.createMessage(message)

                for event in result:
                    webhookData.summary = event['summary']
                    webhookData.description = event.get('description', '')
                    webhookData.eventId = event['id']

                    start = event['start'].get('dateTime','').split('T')
                    if start != ['']:
                        webhookData.date = start[0].replace('-','/')
                        webhookData.time = start[1].replace(':00+09:00','')
                        embeds = webhookContent.createEmbeds(webhookData)

                    body["embeds"].append(embeds)
                webhook.send(body)

        except Exception as e:
            print(e)
                
    def getWeeklyEvents(self):
        try:
            calData = CalendarData()
            calendar = CalendarApi()
            result = calendar.get()

            webhook = Webhook()
            webhookData = WebhookData()
            webhookContent = WebhookContent()

            if result != []:
                message = self.config["webhook"].get('weekly_event_message')
                body = webhookContent.createMessage(message)

                for event in result:
                    webhookData.summary = event['summary']
                    webhookData.description = event.get('description', '')
                    webhookData.eventId = event['id']

                    start = event['start'].get('dateTime','').split('T')
                    if start != ['']:
                        webhookData.date = start[0].replace('-','/')
                        webhookData.time = start[1].replace(':00+09:00','')
                        embeds = webhookContent.createEmbeds(webhookData)
                    else:
                        webhookData.date = event["start"].get("date").replace('-','/')
                        webhookData.endDate = event["end"].get("date").replace('-','/')
                        embeds = webhookContent.createLongEventEmbeds(webhookData)

                    body["embeds"].append(embeds)
                webhook.send(body)

            else:
                message = self.config["webhook"].get('message').get('event_none_message')
                body = webhookContent.createMessage(message)
                webhook.send(body)

        except Exception as e:
            print(e)

    def getDailyEvent(self):
        try:
            calData = CalendarData()
            calendar = CalendarApi()
            result = calendar.get(day=1, routine=False)

            webhook = Webhook()
            webhookData = WebhookData()
            webhookContent = WebhookContent()

            if result != []:
                message = self.config["webhook"].get('message').get('daily_event_message')
                body = webhookContent.createMessage(message)

                for event in result:
                    webhookData.summary = event['summary']
                    webhookData.description = event.get('description', '')
                    webhookData.eventId = event['id']

                    start = event['start'].get('dateTime','').split('T')
                    if start != ['']:
                        webhookData.date = start[0].replace('-','/')
                        webhookData.time = start[1].replace(':00+09:00','')
                        embeds = webhookContent.createEmbeds(webhookData)
                        body["embeds"].append(embeds)
                webhook.send(body)

        except Exception as e:
            print(e)