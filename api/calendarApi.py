import json
import datetime
from google.auth import load_credentials_from_file
from googleapiclient.discovery import build

class CalendarApi():
    def __init__(self):
        with open('config.json', 'r') as f:
            config = json.load(f)
            self.__calendarId = config["calendar"].get('id')

        SCOPES = [config["calendar"].get('calendar')]
        gapi_creds = load_credentials_from_file('credentials.json', SCOPES)[0]
        self.__service = build('calendar', 'v3', credentials=gapi_creds)

    @property
    def calendarUrl(self):
        return self.__calendarUrl

    @property
    def calendarId(self):
        return self.__calendarId

    @property
    def service(self):
        return self.__service

    @property
    def body(self):
        return self.__body

    @body.setter
    def body(self, val):
        self.__body = val

    @property
    def eventId(self):
        return self.__eventId

    @eventId.setter
    def eventId(self, val):
        self.__eventId = val

    def get(self, day=0, routine=False):
        now = datetime.datetime.now(datetime.timezone.utc)

        period = now + datetime.timedelta(days=day)
        if routine:
            timeMax = period + datetime.timedelta(minutes=59)
            timeMax = datetime.datetime(timeMax.year, timeMax.month, timeMax.day, timeMax.hour, timeMax.minutes, tzinfo=datetime.timezone.utc)
        else:
            timeMax = datetime.datetime(period.year, period.month, period.day, 23, 59, tzinfo=datetime.timezone.utc)

        events_result = self.service.events().list(
            calendarId=self.calendarId, 
            timeMin=now.isoformat(),
            timeMax=timeMax.isoformat(),
            maxResults=5,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        return events