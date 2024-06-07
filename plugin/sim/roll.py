import random
from dataclasses import dataclass

from .species import SpeciesData
import datetime
import json


@dataclass
class Roll:
    pass

    # todo 补充补给品类和获取
    def getNonSpecies(self, area: str):
        # 总权重,用于生成随机数种子
        buffSum = 0
        # 从json文件读取类信息,来获取权重总和等信息
        with open(
            "/plugin/sim/data/nonSpecies/NonSpecies.json", "r", encoding="utf-8"
        ) as file:
            data = json.load(file)
        for item in data:
            species = SpeciesData(**item)
            buffSum += self.getSpeciesBuffResult(species, area)
        # 生成1-buffSum之间的随机整数,补给品占比为80%
        suppliesNum = (buffSum * 8) // 10
        # 轮询权重,用来检测落在哪个范围
        rateSum = suppliesNum
        randomNum = random.randint(1, buffSum)
        # 看落在哪个区间,则获取对应的种族
        for item in data:
            species = SpeciesData(**item)
            rateSum += self.getSpeciesBuffResult(species, area)
            if rateSum >= randomNum:
                return species

    # 获取总权重
    def getSpeciesBuffResult(species: SpeciesData, area: str):
        if not species.liveArea.__contains__(area):
            return 0
        timePeriodRateBuff = getTimePeriodRateBuff(species)
        seasonRateBuff = getSeasonRateBuff(species)
        if timePeriodRateBuff == 0 or seasonRateBuff == 0:
            return 0
        return species.baseRateBuff + timePeriodRateBuff + seasonRateBuff


# 获取时间权重
def getTimePeriodRateBuff(species: SpeciesData):
    now = datetime.datetime.now().hour
    if 5 <= now < 10:
        return species.morningRateBuff
    elif 10 <= now < 14:
        return species.noonRateBuff
    elif 14 <= now < 17:
        return species.afternoonRateBuff
    elif 17 <= now <= 24 or 0 <= now < 5:
        return species.nightRateBuff


# 获取季节权重
def getSeasonRateBuff(species: SpeciesData):
    now = datetime.datetime.today().month
    if 3 <= now < 6:
        return species.springRateBuff
    elif 6 <= now < 9:
        return species.summerRateBuff
    elif 9 <= now < 12:
        return species.autumnRateBuff
    elif now == 12 or now == 1 or now == 2:
        return species.winterRateBuff
