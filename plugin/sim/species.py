from sim.globalUtils import *
from sim.ability import Ability


@dataclass
class SpeciesData:
    name: str
    idex: int
    types: list[str]
    abilities: dict[str, Ability]

    """
    出现率相关
    地域
    时间
    季节
    """
    # 我觉得liveArea在这里可以不写，直接在area那里调用找这里的概率就行
    liveArea: list[str]

    baseRateBuff: int

    # 你这个不能写个列表或者字典吗，这样一堆好长
    springRateBuff: int
    summerRateBuff: int
    autumnRateBuff: int
    winterRateBuff: int

    # 这个也是
    morningRateBuff: int
    noonRateBuff: int
    afternoonRateBuff: int
    nightRateBuff: int

    # 时间段,int对应该时段最后时间点
    # class TimePeriod(Enum):
    #     MORNING = "早晨"
    #     NOON = "中午"
    #     AFTERNOON = "下午"
    #     NIGHT = "夜晚"

    # TODO
    pass


def getSpeciesRateBuff(species: SpeciesData):
    species.springRateBuff
    species.nightRateBuff
    # do what you want
    res = 0
    pass
    return res
