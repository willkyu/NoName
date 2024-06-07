import random

from .globalUtils import *
from .data.moveData import moveDataBase
from .item import Rarity
from .player import Player
from .species import SpeciesData
import datetime
from .data.speciesData import speciesDataBase, speciesDataDictCn
from .data.itemData import itemDataWhite, itemDataBlue, itemDataPurple, itemDataGold
from .non import initNonFromSpecies, NON, initMoveSlot, MoveSlot
from .data.livingArea import areaData

ITEAMRATE = 0.8


# todo 补充补给品类和获取
def gacha(player: Player, area: str):
    # 从json文件读取类信息,来获取权重总和等信息
    # * 这里直接从.data.livingArea中读了
    speciesNameCnList = [nonNameCn for nonNameCn in areaData[area]]
    speciesRateBuffList = [
        __getSpeciesBuffResult(speciesDataDictCn[nonNameCn])
        for nonNameCn in speciesNameCnList
    ]

    # 补给品占比为80%
    # 如果随机数小于补给品数值，则此次获得物品
    if random.random() <= ITEAMRATE:
        return __getRandomItems(player)

    gotNonNameCn = random.choices(speciesNameCnList, speciesRateBuffList)
    # 获得Non
    return __getNon(speciesDataDictCn[gotNonNameCn], player)


def __getNon(species: SpeciesData, player: Player):
    # 调用丘丘提供的Non实例方法然后复写其中的随机属性
    non = initNonFromSpecies(species)
    # 设置随机ability
    non.ability = species.abilities.__getattribute__(
        random.choice(
            list(species.abilities.__dict__.keys()) - ["H"]
            if hiddenAbilityAvailable
            else []
        )
    )
    non.gender = (
        "N"
        if species.generRate == None
        else ("M" if random.random() > species.generRate else "F")
    )
    non.ivs = IVs(**{stat: random.randint(0, 31) for stat in statList})

    # 随机技能列表
    non.moveSlots = {
        moveName: MoveSlot(moveName)
        for moveName in random.sample(list(species.moveLearnSet.values()), 4)
    }

    non.masterId = player.id
    non.save()  # 这时候会保存在暂存区，等待命名


def __getRandomItems(player: Player):
    # 物品分稀有度等级，按照稀有度排序，和为1，生成0-1随机浮点看落在哪个区间
    random_result = random.random()
    if 0 <= random_result < Rarity.WHITE:
        item = random.choice(itemDataWhite)
    elif Rarity.WHITE <= random_result < Rarity.WHITE + Rarity.BLUE:
        item = random.choice(itemDataBlue)
    elif (
        Rarity.WHITE + Rarity.BLUE
        <= random_result
        < Rarity.WHITE + Rarity.BLUE + Rarity.PURPLE
    ):
        item = random.choice(itemDataPurple)
    else:
        item = random.choice(itemDataGold)
    # todo 更加item归属层
    item.mas


# 获取总权重
def __getSpeciesBuffResult(species: SpeciesData):
    timePeriodRateBuff = getTimePeriodRateBuff(species)
    seasonRateBuff = getSeasonRateBuff(species)
    return species.baseRateBuff * timePeriodRateBuff * seasonRateBuff


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
