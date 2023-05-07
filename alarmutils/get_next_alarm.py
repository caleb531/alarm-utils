#!/usr/bin/env python3

from datetime import datetime, timedelta
from typing import Sequence

from alarmutils.alarm import Alarm
from alarmutils.exceptions import NextAlarmRingTimeNotFound


# The number of days in a week
DAYS_IN_WEEK = 7


def alarm_allowed_on_datetime(alarm: Alarm, some_datetime: datetime) -> bool:
    weekday = some_datetime.strftime('%a').lower()
    return ((not alarm.repeat or weekday in alarm.repeat) and
            some_datetime > datetime.now())


def get_alarm_next_ring_time(alarm: Alarm) -> datetime:

    next_datetime = datetime.combine(
        date=datetime.today(),
        time=alarm.time)
    # We don't need to search any farther out than one week
    for i in range(DAYS_IN_WEEK + 1):
        if alarm_allowed_on_datetime(alarm, next_datetime):
            return next_datetime
        next_datetime = next_datetime + timedelta(days=1)
    # Every enabled alarm is logically guaranteed to have a Next Ring Time, so
    # if it doesn't, there is a bug in the code
    raise NextAlarmRingTimeNotFound(f'Next Ring Time not found for: {alarm}')


# Get the alarm that will ring next
def get_next_alarm(alarms: Sequence[Alarm]):
    try:
        return min(
            (alarm for alarm in alarms if alarm.enabled),
            key=get_alarm_next_ring_time)
    except ValueError:
        return None
