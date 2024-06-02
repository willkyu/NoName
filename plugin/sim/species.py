from sim.globalUtils import *
from sim.ability import Ability
from enum import Enum
import datetime


@dataclass
class SpeciesData:
    name: str
    idex: int
    types: list[str]
    abilities: dict[str, Ability]

    '''
    出现率相关
    地域
    时间
    季节
    '''
    liveArea: list[str]

    baseRateBuff: int

    springRateBuff: int
    summerRateBuff: int
    autumnRateBuff: int
    winterRateBuff: int

    morningRateBuff: int
    noonRateBuff: int
    afternoonRateBuff: int
    nightRateBuff: int

    def getBuffResult(self, area: str):
        if self.liveArea.__contains__(area):
            return self.baseRateBuff + self.getSeasonRateBuff() + self.getSeasonRateBuff()
        else:
            return 0

    def getTimePeriodRateBuff(self):
        now = datetime.datetime.now().hour
        if 5 <= now < 10:
            return self.morningRateBuff
        elif 10 <= now < 14:
            return self.noonRateBuff
        elif 14 <= now < 17:
            return self.afternoonRateBuff
        elif 17 <= now <= 24 or 0 <= now < 5:
            return self.nightRateBuff

    def getSeasonRateBuff(self):
        now = datetime.datetime.today().month
        if 3 <= now < 6:
            return self.springRateBuff
        elif 6 <= now < 9:
            return self.summerRateBuff
        elif 9 <= now < 12:
            return self.autumnRateBuff
        elif now == 12 or now == 1 or now == 2:
            return self.winterRateBuff

    # 时间段,int对应该时段最后时间点
    # class TimePeriod(Enum):
    #     MORNING = "早晨"
    #     NOON = "中午"
    #     AFTERNOON = "下午"
    #     NIGHT = "夜晚"

    # TODO
    pass
