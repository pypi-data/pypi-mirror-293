import dataclasses
import datetime

from reg_shared_lib.data import Event as _Event


@dataclasses.dataclass
class Event(_Event):
    pass


@dataclasses.dataclass
class Unit:
    id: int
    name: str


@dataclasses.dataclass
class Action:
    id: int
    name: str
    unit: Unit | None
    number: int
    off_schedule: bool
    off_schedule_location: str | None
    draft_comment: str
    required_minimum_age: int
    principal_name: str


@dataclasses.dataclass
class Place:
    id: int
    name: str


@dataclasses.dataclass
class Lot:
    id: int
    date: datetime.date
    place: Place
    act_start: datetime.datetime
    act_stop: datetime.datetime
    actions: list[int]


@dataclasses.dataclass
class Draft:
    event: Event
    actions: list[Action]
    lots: list[Lot]

    def __post_init__(self):
        for lot in self.lots:
            lot.act_start = lot.act_start.astimezone(self.event.timezone)
            lot.act_stop = lot.act_stop.astimezone(self.event.timezone)


@dataclasses.dataclass
class Plan:
    event: Event
    actions: list[Action]
