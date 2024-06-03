from enum import Enum
from typing import Literal


# 出现区域
class Area(Enum):
    PLAIN = "平原"
    MOUNTAIN = "山岭"
    SEA = "海洋"
    SWAMP = "沼泽"
    DESERT = "沙漠"


# 这样写怎么样？
AreaType = Literal["平原", "山岭", "海洋", "沼泽", "沙漠"]


class Area:
    type: AreaType
    existingSpecies: list
