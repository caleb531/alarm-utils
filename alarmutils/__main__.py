#!/usr/bin/env python3

import argparse
import json

from alarmutils.alarm import Alarm

from alarmutils.get_next_alarm import get_next_alarm


def get_cli_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('alarms_file_path', metavar='alarms_file')
    return parser.parse_args()


def read_alarms_from_file(alarms_file_path: str):
    with open(alarms_file_path, 'r') as alarms_file:
        return [Alarm(**alarm_dict) for alarm_dict in json.load(alarms_file)]


def main() -> None:

    cli_args = get_cli_args()
    alarms = read_alarms_from_file(cli_args.alarms_file_path)
    print(get_next_alarm(alarms))


if __name__ == '__main__':
    main()
