#!/usr/bin/env python3

import unittest

from alarmutils.alarm import Alarm
from alarmutils.get_next_alarm import get_next_alarm


class TestGetNextAlarm(unittest.TestCase):
    """Tests for alarmutils.get_next_alarm()"""

    def test_all_alarms_disabled(self) -> None:
        """Should return None if all alarms are disabled."""
        self.assertEqual(get_next_alarm([
            Alarm(time='7:30am', enabled=False),
            Alarm(time='7:40am', enabled=False)
        ]), None)


if __name__ == '__main__':
    unittest.main()
