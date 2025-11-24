#!/usr/bin/env python3

import pytest
from freezegun import freeze_time

from alarmutils.alarm import Alarm
from alarmutils.get_next_alarm import NextAlarmRingTimeNotFound, get_next_alarm


def _assert_next_alarm(alarms: list[Alarm], next_alarm_index: int) -> None:
    assert get_next_alarm(alarms) == alarms[next_alarm_index]


def test_all_alarms_disabled() -> None:
    """Should return None if all alarms are disabled."""
    assert (
        get_next_alarm(
            [
                Alarm(time="7:30am", enabled=False),
                Alarm(time="7:40am", enabled=False),
            ]
        )
        is None
    )


@freeze_time("7:15am")
def test_today() -> None:
    """Should get next alarm for a time today that has not yet elapsed."""
    _assert_next_alarm(
        alarms=[
            Alarm(time="7:00am", enabled=True),
            Alarm(time="7:30am", enabled=True),
            Alarm(time="8:00am", enabled=True),
        ],
        next_alarm_index=1,
    )


@freeze_time("8:15am")
def test_tomorrow() -> None:
    """Should get alarm for tomorrow if time today has already elapsed."""
    _assert_next_alarm(
        alarms=[
            Alarm(time="7:00am", enabled=True),
            Alarm(time="7:30am", enabled=True),
            Alarm(time="8:00am", enabled=True),
        ],
        next_alarm_index=0,
    )


@freeze_time("8:15am")
def test_tomorrow_ignore_disabled() -> None:
    """Should get alarm for tomorrow ignoring disabled alarms."""
    _assert_next_alarm(
        alarms=[
            Alarm(time="7:00am", enabled=False),
            Alarm(time="7:30am", enabled=True),
            Alarm(time="8:00am", enabled=True),
        ],
        next_alarm_index=1,
    )


@freeze_time("2023-01-02 6:30am")  # 2023-01-02 is a Monday
def test_repeat_on_today() -> None:
    """Should get alarm for today if repeat falls on today."""
    _assert_next_alarm(
        alarms=[
            Alarm(time="7:00am", enabled=True, repeat=["sun"]),
            Alarm(time="7:30am", enabled=True, repeat=["mon"]),
            Alarm(time="8:00am", enabled=True, repeat=["sun"]),
        ],
        next_alarm_index=1,
    )


@freeze_time("2023-01-03 8:15am")  # 2023-01-03 is a Tuesday
def test_repeat_later_this_week() -> None:
    """Should get alarm that falls on a weekday later this week."""
    _assert_next_alarm(
        alarms=[
            Alarm(time="7:30am", enabled=True, repeat=["thu"]),
            Alarm(time="8:00am", enabled=True, repeat=["wed"]),
            Alarm(time="8:00am", enabled=True, repeat=["mon"]),
            Alarm(time="8:00am", enabled=True, repeat=["tue"]),
        ],
        next_alarm_index=1,
    )


@freeze_time("2023-01-01 7:15am")  # 2023-01-01 is a Sunday
def test_next_alarm_a_week_away() -> None:
    """Should get alarm that falls on a weekday later this week."""
    _assert_next_alarm(
        alarms=[Alarm(time="8:00am", enabled=True, repeat=["sun"])],
        next_alarm_index=0,
    )


def test_logical_error() -> None:
    """Should raise error if no enabled alarms."""
    with pytest.raises(NextAlarmRingTimeNotFound):
        get_next_alarm([Alarm(time="8:00am", enabled=True, repeat=["xyz"])])
