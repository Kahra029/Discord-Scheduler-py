import os
import re
import json
import schedule
import discord
from time import sleep
from logic.pixivwork import PixivWork
from logic.calendarLogic import CalendarLogic

with open('config.json', 'r') as f:
    config = json.load(f)
discordToken = config['discord_token']
calendarText = config['calendar'].get('calendar_text')
listText = config['calendar'].get('list_text')
startText = config['calendar'].get('start_text')
longEventText = config['calendar'].get('long_event_text')
deleteText = config['calendar'].get('delete_text')

client = discord.Client(ws = int(os.environ.get('PORT', 5000)))

@client.event
async def on_ready():
    print('READY')

@client.event
async def on_message(message):
    content = message.content

    if content == calendarText:
        logic = CalendarLogic()
        result = logic.calendarUrl()

    if content == listText:
        logic = CalendarLogic()
        result = logic.get()
        
    elif re.search(startText, content):
        event = content.replace(startText, '')
        logic = CalendarLogic()
        logic.insert(event)

    elif re.search(longEventText, content):
        event = content.replace(longEventText, '')
        logic = CalendarLogic()
        logic.insertLongEvent(event)

    elif re.search(deleteText, content):
        eventId = content.replace(deleteText, '')
        logic = CalendarLogic()
        logic.delete(eventId)

client.run(discordToken)

