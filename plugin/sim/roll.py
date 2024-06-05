import random
from species import SpeciesData
import datetime
from data.speciesData import speciesDataBase
from data.itemData import itemDataBase


# todo 补充补给品类和获取
def gacha(self, area: str):
    # 总权重,用于生成随机数种子
    buff_sum = 0
    # 从json文件读取类信息,来获取权重总和等信息

    for item in speciesDataBase:
        buff_sum += self.getSpeciesBuffResult(item, area)
    # 生成1-buffSum之间的随机整数,补给品占比为80%
    supplies_num = (buff_sum * 8) // 10
    # 轮询权重,用来检测落在哪个范围
    random_num = random.randint(1, supplies_num + buff_sum)
    # 如果随机数小于补给品数值，则此次获得物品
    if random_num <= supplies_num:
        return __getRandomItemsInstance()

    # 如果随机数大于补给品数值，则获得Non
    rate_sum = supplies_num
    # 看落在哪个区间,则获取对应的种族
    for item in speciesDataBase:
        rate_sum += self.getSpeciesBuffResult(item, area)
        if rate_sum >= random_num:
            return __getNonInstance(item)


def __getNonInstance(species: SpeciesData):
    # 调用丘丘提供的Non实例方法然后复写其中的随机属性
    pass


def __getRandomItemsInstance():
    # 物品分稀有度等级，按照稀有度排序，和为1，生成0-1随机浮点看落在哪个区间
    random_result = random.random()



    for item in itemDataBase:
        pass
    pass


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
