from dataclasses import dataclass, field
from enum import Enum
from typing import Callable

from .non_events import NonEventsObj

SpecialEffectClass = Callable | str | None  # 特殊效果，还没想好是函数还是字符串


# @dataclass
# class Rarity():
#     WHITE = 0.5
#     BLUE = 0.3
#     PURPLE = 0.15
#     GOLD = 0.05

class Rarity(Enum):
    WHITE = 0.5
    BLUE = 0.3
    PURPLE = 0.15
    GOLD = 0.05


@dataclass
class ItemData:
    """和ability差不多"""

    id: int 
    # 招式名
    name: str
    name_cn: str

    # 稀有度
    rarity: Rarity
    # description
    desc: str
    # 是否是消耗品
    consumable: bool = False
    # 一些布尔型flag
    flags: dict[str, bool] = field(default_factory=dict)
    
    add_non_events: NonEventsObj = field(default_factory=NonEventsObj)

    # # TODO
    # def __post_init__(self):
    #     if self.flags is None:
    #         self.flags = {}
    #     if self.add_non_events is None:
    #         self.add_non_events = NonEventsObj()

    def __str__(self) -> str:
        return self.name_cn

    # TODO
    pass
