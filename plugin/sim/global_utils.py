from dataclasses import dataclass
from typing import Literal, Annotated
from configparser import ConfigParser
from json import dump
import os

import requests


from .data.move_data import move_data_dict_cn, move_data_dict_en

BattleMode = Literal["single", "double", "chaos4"]
battle_mode = ["single", "double", "chaos4"]
battle_mode_dsc = ["单打", "双打", "四人乱战"]


BASE_NON_FILE_PATH = "./plugin/data/NoName/data/"


@dataclass
class Range:
    min: int
    max: int


def make_sure_dir(path: str) -> None:
    if not os.path.exists(path):
        os.mkdir(path)


make_sure_dir(BASE_NON_FILE_PATH)

conf = ConfigParser()


def read_coin(user_id):
    path = "./plugin/data/ChanceCustom/Mance/数据/背包/{}.ini".format(user_id)
    if os.path.exists(path):
        conf.read(
            path,
            encoding="utf-8",
        )
        return int(conf["背包"]["coin"])
    return 0


def write_coin(user_id, coin):
    path = "./plugin/data/ChanceCustom/Mance/数据/背包/{}.ini".format(user_id)
    if os.path.exists(path):
        conf.read(
            path,
            encoding="utf-8",
        )
        conf["背包"]["coin"] = str(coin)
        with open(path, "w", encoding="utf-8") as f:
            conf.write(f)
    return


def create_new_config(player_id: str):
    """为新玩家创建配置文件

    Args:
        playerId (str): _description_
    """
    newdict = {
        "id": player_id,
        "path": BASE_NON_FILE_PATH + "{}/".format(player_id),
        "team": [],
        "dream_crystal": 0,
        "bag": {},
    }
    make_sure_dir(newdict["path"])
    with open(newdict["path"] + "userConfig.json", "w+", encoding="utf-8") as f:
        dump(newdict, f, ensure_ascii=False)


def get_nickname(qqId: str) -> str:
    try:
        return eval(
            requests.get(
                "https://api.oioweb.cn/api/qq/info?qq={}".format(qqId), timeout=(1, 2)
            ).content.decode("utf-8")
        )["result"]["nickname"]
    except requests.RequestException:
        return qqId


def get_move_en(move_name_en: str):
    return move_data_dict_en[move_name_en]


def getMoveCn(move_name_cn: str):
    return move_data_dict_cn[move_name_cn]


LevelRange = Annotated[int, Range(1, 100)]
IvRange = Annotated[int, Range(0, 31)]
EvRange = Annotated[int, Range(0, 252)]
StatsLevelRange = Annotated[int, Range(-6, 6)]

stat_list = ["HP", "ATK", "DEF", "SPA", "SPD", "SPE"]
Type = str

# 隐藏特性开启flag-活动事件
hidden_ability_available = False


@dataclass
class IVs:
    HP: IvRange = 0
    ATK: IvRange = 0
    DEF: IvRange = 0
    SPA: IvRange = 0
    SPD: IvRange = 0
    SPE: IvRange = 0


@dataclass
class StatLevel:
    ATK: StatsLevelRange = 0
    DEF: StatsLevelRange = 0
    SPA: StatsLevelRange = 0
    SPD: StatsLevelRange = 0
    SPE: StatsLevelRange = 0
    ACC: StatsLevelRange = 0
    EVA: StatsLevelRange = 0


@dataclass
class StatValue:
    ATK: int = 0
    DEF: int = 0
    SPA: int = 0
    SPD: int = 0
    SPE: int = 0


@dataclass
class EVs:
    HP: EvRange = 0
    ATK: EvRange = 0
    DEF: EvRange = 0
    SPA: EvRange = 0
    SPD: EvRange = 0
    SPE: EvRange = 0

    def changeEv(self, ev: str, num: int, add_mode: bool = True):
        if ev.upper() not in stat_list:
            print("Ev not valid!")
            return
        eval("self.{}{}={}".format(ev.upper(), "+" if add_mode else "-", num))
