import schedule
import time
from logic.schedulerLogic import SchedulerLogic


def EventSchedule():
    logic = SchedulerLogic()
    schedule.every().monday.at("08:45").do(logic.getWeeklyEvents)
    schedule.every().day.at("09:00").do(logic.getDailyEvent)
    schedule.every(1).hour.at(":00").do(logic.getEvent)

EventSchedule()

while True:
    schedule.run_pending()
    time.sleep(1)