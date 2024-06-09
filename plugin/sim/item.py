from dataclasses import dataclass, field
from enum import Enum
from typing import Callable

from .non_events import NonEventsObj

SpecialEffectClass = Callable | str | None  # 特殊效果，还没想好是函数还是字符串


class Rarity(Enum):
    WHITE = 0.5
    BLUE = 0.3
    PURPLE = 0.15
    GOLD = 0.05


rarity_list = list(Rarity.__members__.keys())


@dataclass
class ItemData:
    """和ability差不多"""

    id: int
    # 招式名
    name: str
    name_cn: str

    # 稀有度
    rarity: str
    # description
    desc: str
    # 是否是消耗品，战斗中的消耗
    consumable: bool = False
    # 直接使用
    can_be_use: bool = False
    # 一些布尔型flag
    flags: dict[str, bool] = field(default_factory=dict)

    add_non_events: NonEventsObj = field(default_factory=NonEventsObj)

    # TODO
    # def __post_init__(self):
    #     if self.flags is None:
    #         self.flags = {}
    #     if self.add_non_events is None:
    #         self.add_non_events = NonEventsObj()

    def __str__(self) -> str:
        item_str = ""
        item_str += f"{self.name_cn} {self.name} 稀有度: {self.rarity}\n"
        item_str += "可以直接使用.\n" if self.can_be_use else ""
        item_str += self.desc
        return item_str

    # TODO
    pass
