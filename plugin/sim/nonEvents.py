from __future__ import annotations
from typing import Callable, Literal
from dataclasses import dataclass

from sim.globalUtils import *

"""
* Simple字段的类只是用来类型提示的，没有其他作用
"""


@dataclass
class SimpleNON:
    name: str
    masterId: str
    species: Literal["SpeciesData"]
    level: LevelRange
    gender: Literal["M", "F", "N"]
    inBattle: str  # should be '' if not in battle
    item: str
    battleStatus: Literal["NonTempBattleStatus"]
    ability: Literal["Ability"]
    nonEvents: Literal["NonEvents"]

    moveSlots: list[Literal["MoveSlot"]]
    ivs: IVs
    evs: EVs

    statDict: dict[str, int]


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
    reason: str
    exe: Callable[[SimpleField, dict[str, object]], None]

    def exe(self, field: SimpleField, **kwargs):
        pass


def nonEventFunExample(field: SimpleField, **kwargs):
    """一个例子"""
    if field.weather == "Rainy":
        field.log.append("天气没有任何变化……\n")
        return
    field.weather = "Rainy"
    field.log.append("天气变成了雨天……\n")

    field.eventTrigger(field, "onWeatherChanged", **kwargs)
    pass


nonEventExample = NonEvent("MakeRain Ability", nonEventFunExample)  # 一个例子

defaultNonEvent = NonEvent("")


@dataclass
class NonEventsObj:
    beforeSwitch: NonEvent = None
    afterSwitch: NonEvent = None
    onWeatherChanged: NonEvent = None

    def __post_init__(self) -> None:
        for k in self.__dict__.keys():
            self.__setattr__(k, defaultNonEvent)
        pass
