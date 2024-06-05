from __future__ import annotations
from typing import Callable, Literal
from dataclasses import dataclass
from functools import partial

# from sim.globalUtils import *

"""
* Simple字段的类只是用来类型提示的，没有其他作用
"""


@dataclass
class StatsLevel:
    ATK: int = 0
    DEF: int = 0
    SPA: int = 0
    SPD: int = 0
    SPE: int = 0
    ACC: int = 0
    EVA: int = 0


@dataclass
class SimpleNON:
    name: str
    masterId: str
    species: Literal["SpeciesData"]
    level: Literal["LevelRange"]
    gender: Literal["M", "F", "N"]
    inBattle: str  # should be '' if not in battle
    item: str
    battleStatus: Literal["NonTempBattleStatus"]
    ability: Literal["Ability"]
    nonEvents: Literal["NonEvents"]

    moveSlots: list[Literal["MoveSlot"]]

    statsLevel: StatsLevel


@dataclass
class SimpleSide:
    nonNum: Literal[1, 2]
    activeNons: list[SimpleNON]
    notActiveNons: list[SimpleNON]

    commandList: dict[int, Literal["Command"]]

    # 一些其他的东西，如护盾
    shield: bool = False


@dataclass
class SimpleField:
    sides: dict[str, SimpleSide]  # {userId: Side}
    nonTeamDict: dict[str, list[SimpleNON]]  # {userId:[NON]}
    log: list[str]

    eventTrigger: Callable[[SimpleField, str, list | None], None]
    weather: str = "Normal"

    # 一些其他的东西
    lastUsedMove: str | None = None


@dataclass
class NonEvent:
    reason: str = None
    exe: Callable[[SimpleField, dict[str, object]], None] = None

    def __post_init__(self):
        if self.exe == None:
            self.exe = self.defaultExe
        else:
            self.exe = partial(self.exe, self)

    def defaultExe(self, field: SimpleField, **kwargs):
        pass


def nonEventFunExample(self: NonEvent, field: SimpleField, **kwargs):
    field.updateWeather("Rainy", reason="Rainy Ability", **kwargs)

    # """一个例子"""
    # if field.weather == "Rainy":
    #     field.log.append("天气没有任何变化……\n")
    #     return
    # field.weather = "Rainy"
    # field.log.append("天气变成了雨天……\n")

    # field.eventTrigger(field, "onWeatherChanged", **kwargs)
    # pass


nonEventExample = NonEvent("MakeRain Ability", nonEventFunExample)  # 一个例子


@dataclass
class NonEventsObj:
    onActiveOnce: NonEvent = None
    beforeSwitch: NonEvent = None
    afterSwitch: NonEvent = None
    onWeatherChanged: NonEvent = None

    def __post_init__(self) -> None:
        for k in self.__dict__.keys():
            if self.__getattribute__(k) is None:
                self.__setattr__(k, NonEvent())
        pass
