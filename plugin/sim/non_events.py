from __future__ import annotations
from typing import Callable, TYPE_CHECKING
from dataclasses import dataclass
from functools import partial
from collections import UserList

if TYPE_CHECKING:
    from sim.field import Field


@dataclass
class NonEvent:
    reason: str = None
    exe: Callable[[Field, dict[str, object]], None] = None

    def __post_init__(self):
        if self.exe is None:
            self.exe = self.default_exe
        else:
            self.exe = partial(self.exe, self)

    def default_exe(self, field: Field, **kwargs):
        pass


class NonEventList(UserList):
    def exe(self, field: Field, **kwargs):
        # for i in range(len(self)):
            # super().__getitem__(i).exe(field, **kwargs)
        for event in self:
            event.exe(field, **kwargs)


@dataclass
class NonEventsObj:
    on_active_once: NonEventList = None
    before_switch: NonEventList = None
    after_switch: NonEventList = None
    on_weather_changed: NonEventList = None
    end_of_turn: NonEventList = None
    start_of_turn: NonEventList = None
    on_get: NonEventList = None
    on_hit: NonEventList = None

    def __post_init__(self) -> None:
        for k in self.__dict__.keys():
            if self.__getattribute__(k) is None:
                self.__setattr__(k, NonEventList())
        pass
