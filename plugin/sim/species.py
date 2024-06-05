from sim.globalUtils import *
from sim.ability import Ability, SpeciesAbilities


@dataclass
class RateBuff:
    springRateBuff: int
    summerRateBuff: int
    autumnRateBuff: int
    winterRateBuff: int

    # 时间段,int对应该时段最后时间点
    # class TimePeriod(Enum):
    #     MORNING = "早晨"
    #     NOON = "中午"
    #     AFTERNOON = "下午"
    #     NIGHT = "夜晚"
    morningRateBuff: int
    noonRateBuff: int
    afternoonRateBuff: int
    nightRateBuff: int


@dataclass
class SpeciesStrength:
    HP: int = 0
    ATK: int = 0
    DEF: int = 0
    SPA: int = 0
    SPD: int = 0
    SPE: int = 0


@dataclass
class SpeciesData:
    name: str
    idex: int
    types: list[str]
    abilities: SpeciesAbilities
    speciesStrength: SpeciesStrength

    """
    出现率相关
    地域
    时间
    季节
    """
    # 我觉得liveArea在这里可以不写，直接在area那里调用找这里的概率就行
    liveArea: list[str]

    baseRateBuff: int = 5

    rateBuff: RateBuff = None

    # TODO
    pass


def getSpeciesRateBuff(species: SpeciesData):
    species.rateBuff.springRateBuff
    species.rateBuff.nightRateBuff
    # do what you want
    res = 0
    pass
    return res
