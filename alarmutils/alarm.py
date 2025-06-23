#!/usr/bin/env python3

import datetime
from dataclasses import dataclass
from typing import Literal, Optional, Union

WeekdayT = Union[
    Literal["sun"],
    Literal["mon"],
    Literal["tue"],
    Literal["wed"],
    Literal["thu"],
    Literal["fri"],
    Literal["sat"],
]


@dataclass
class Alarm(object):
    label: str
    time: datetime.time
    enabled: bool
    repeat: Optional[list[WeekdayT]]

    def __init__(
        self,
        *,
        time: str,
        enabled: bool,
        label: str = "Alarm",
        repeat: list[WeekdayT] = None,
    ) -> None:
        self.time = datetime.datetime.strptime(time, "%I:%M%p").time()
        self.enabled = enabled
        self.label = label
        self.repeat = repeat
