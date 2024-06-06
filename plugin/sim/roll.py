import random

import globalUtils
from sim.data.moveData import moveDataBase
from sim.item import Rarity
from sim.player import Player
from species import SpeciesData
import datetime
from data.speciesData import speciesDataBase
from data.itemData import itemDataWhite, itemDataBlue, itemDataPurple, itemDataGold
from non import initNonFromSpecies, NON, initMoveSlot


# todo 补充补给品类和获取
def gacha(area: str, player: Player):
    # 总权重,用于生成随机数种子
    buff_sum = 0
    # 从json文件读取类信息,来获取权重总和等信息
    for item in speciesDataBase:
        buff_sum += __getSpeciesBuffResult(item, area)
    # 生成1-buffSum之间的随机整数,补给品占比为80%
    supplies_num = (buff_sum * 8) // 10
    # 轮询权重,用来检测落在哪个范围
    random_num = random.randint(1, supplies_num + buff_sum)
    # 如果随机数小于补给品数值，则此次获得物品
    if random_num <= supplies_num:
        return __getRandomItems(player)

    # 如果随机数大于补给品数值，则获得Non
    rate_sum = supplies_num
    # 看落在哪个区间,则获取对应的种族
    for item in speciesDataBase:
        rate_sum += __getSpeciesBuffResult(item, area)
        if rate_sum >= random_num:
            return __getNon(item, player)


def __getNon(species: SpeciesData, player: Player):
    # 调用丘丘提供的Non实例方法然后复写其中的随机属性
    non = initNonFromSpecies(species)
    # 设置随机ability
    randomNum = random.random()
    if globalUtils.hiddenAbilityAvailable:
        if 0 <= randomNum < 0.4:
            # 大于0.5选A1 否则选A2
            non.ability = species.abilities.A1
        elif 0.4 <= randomNum < 0.8:
            non.ability = species.abilities.A2
        else:
            non.ability = species.abilities.H
    else:
        if randomNum > 0.5:
            # 大于0.5选A1 否则选A2
            non.ability = species.abilities.A1
        else:
            non.ability = species.abilities.A2
    # 随机技能列表
    moveSlotDict = {}
    moveDataAmount = len(moveDataBase)
    for i in range(4):
        randomMoveDataNum = random.randint(0, moveDataAmount - 1)
        moveSlot = initMoveSlot(moveDataBase[randomMoveDataNum])
        moveSlotDict[moveSlot.name] = moveSlot
    non.moveSlots = moveSlotDict
    non.masterId = player.id
    non.save()


def __getRandomItems(player: Player):
    # 物品分稀有度等级，按照稀有度排序，和为1，生成0-1随机浮点看落在哪个区间
    random_result = random.random()
    if 0 <= random_result < Rarity.WHITE:
        item = random.choice(itemDataWhite)
    elif Rarity.WHITE <= random_result < Rarity.WHITE + Rarity.BLUE:
        item = random.choice(itemDataBlue)
    elif Rarity.WHITE + Rarity.BLUE <= random_result < Rarity.WHITE + Rarity.BLUE + Rarity.PURPLE:
        item = random.choice(itemDataPurple)
    else:
        item = random.choice(itemDataGold)
    # todo 更加item归属层
    item.mas


# 获取总权重
def __getSpeciesBuffResult(species: SpeciesData, area: str):
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
        return species.rateBuff.morningRateBuff
    elif 10 <= now < 14:
        return species.rateBuff.noonRateBuff
    elif 14 <= now < 17:
        return species.rateBuff.afternoonRateBuff
    elif 17 <= now <= 24 or 0 <= now < 5:
        return species.rateBuff.nightRateBuff


# 获取季节权重
def getSeasonRateBuff(species: SpeciesData):
    now = datetime.datetime.today().month
    if 3 <= now < 6:
        return species.rateBuff.springRateBuff
    elif 6 <= now < 9:
        return species.rateBuff.summerRateBuff
    elif 9 <= now < 12:
        return species.rateBuff.autumnRateBuff
    elif now == 12 or now == 1 or now == 2:
        return species.rateBuff.winterRateBuff
