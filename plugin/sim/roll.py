import random

from .global_utils import hidden_ability_available, stat_list, write_coin

from .item import Rarity, rarity_list
from .player import Player
from .species import SpeciesData
import datetime
from .data.species_data import species_data_dict_cn
from .data.item_data import item_data_rarity
from .non import init_non_from_species, MoveSlot, IVs
from .data.living_area import area_data

ITEAMRATE = 0.8


# todo 补充补给品类和获取
def gacha(player: Player, area: str, mode: str = "normal"):
    if mode == "normal":
        if player.coin >= 100:
            write_coin(player.id, player.coin - 100)
        else:
            return False

    # 从json文件读取类信息,来获取权重总和等信息
    # * 这里直接从.data.livingArea中读了
    species_name_cn_list = [non_name_cn for non_name_cn in area_data[area]]
    species_rate_buff_list = [
        __get_species_buff_result(species_data_dict_cn[non_name_cn])
        for non_name_cn in species_name_cn_list
    ]

    # 补给品占比为80%
    # 如果随机数小于补给品数值，则此次获得物品
    if random.random() <= ITEAMRATE:
        return __get_random_items(player)

    got_non_name_cn = random.choices(species_name_cn_list, species_rate_buff_list)[0]
    # 获得Non
    return __getNon(species_data_dict_cn[got_non_name_cn], player)


def __getNon(species: SpeciesData, player: Player):
    # 调用丘丘提供的Non实例方法然后复写其中的随机属性
    non = init_non_from_species(species)
    # 设置随机ability
    non.ability = species.abilities.__getattribute__(
        random.choice(
            list(
                set(species.abilities.__dict__.keys())
                - (set("H") if hidden_ability_available else set())
            )
        )
    )
    non.gender = (
        "N"
        if species.gender_rate is None
        else ("M" if random.random() > species.gender_rate else "F")
    )
    non.ivs = IVs(**{stat: random.randint(0, 31) for stat in stat_list})

    # 随机技能列表
    non.move_slots = {
        move_name: MoveSlot(move_name)
        for move_name in random.sample(
            list(species.move_learn_set.values()), min(4, len(species.move_learn_set))
        )
    }

    non.master_id = player.id
    non.save()  # 这时候会保存在暂存区，等待命名
    return f"NON(Lv.{non.level}): {non.species.name_cn}"


def __get_random_items(player: Player):
    # 物品分稀有度等级，按照稀有度排序，和为1，生成0-1随机浮点看落在哪个区间
    rarity_list_except_empty = [
        rarity for rarity in rarity_list if len(item_data_rarity[rarity]) > 0
    ]
    rarity_rate_list = [Rarity[rarity].value for rarity in rarity_list_except_empty]
    rarity = random.choices(rarity_list_except_empty, rarity_rate_list)[0]
    item = random.choice(item_data_rarity[rarity])

    player.set_item(item, player.bag[item] + 1)
    return f"物品({rarity}): {item}"


# 获取总权重
def __get_species_buff_result(species: SpeciesData):
    time_period_rate_buff = get_time_period_rate_buff(species)
    season_rate_buff = get_season_rate_buff(species)
    return species.base_rate_buff * time_period_rate_buff * season_rate_buff


# 获取时间权重
def get_time_period_rate_buff(species: SpeciesData):
    now = datetime.datetime.now().hour
    if 5 <= now < 10:
        return species.rate_buff.morning_rate_buff
    elif 10 <= now < 14:
        return species.rate_buff.noon_rate_buff
    elif 14 <= now < 17:
        return species.rate_buff.afternoon_rate_buff
    elif 17 <= now <= 24 or 0 <= now < 5:
        return species.rate_buff.night_rate_buff


# 获取季节权重
def get_season_rate_buff(species: SpeciesData):
    now = datetime.datetime.today().month
    if 3 <= now < 6:
        return species.rate_buff.spring_rate_buff
    elif 6 <= now < 9:
        return species.rate_buff.summer_rate_buff
    elif 9 <= now < 12:
        return species.rate_buff.autumn_rate_buff
    elif now == 12 or now == 1 or now == 2:
        return species.rate_buff.winter_rate_buff
