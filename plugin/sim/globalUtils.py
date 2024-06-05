from dataclasses import dataclass
from typing import Literal, Callable, Annotated
from configparser import ConfigParser
from json import dump, load
import os

import requests


from sim.data.moveData import *

BattleMode = Literal["single", "double", "chaos4"]

baseNonFilePath = "./plugin/data/NoName/data/"


@dataclass
class Range:
    min: int
    max: int


def makeSureDir(path: str) -> None:
    if not os.path.exists(path):
        os.mkdir(path)


conf = ConfigParser()


def readCoin(user_id):
    path = "./plugin/data/ChanceCustom/Mance/数据/背包/{}.ini".format(user_id)
    if os.path.exists(path):
        conf.read(
            path,
            encoding="utf-8",
        )
        return int(conf["背包"]["coin"])
    return 0


def writeCoin(user_id, coin):
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


def createNewConfig(playerId: str):
    """为新玩家创建配置文件

    Args:
        playerId (str): _description_
    """
    newdict = {
        "id": playerId,
        "path": baseNonFilePath + "{}/".format(playerId),
        "team": [],
        "dreamCrystal": 0,
    }
    makeSureDir(newdict["path"])
    with open(newdict["path"] + "userConfig.json", "w+") as f:
        dump(newdict, f)


def getNickname(qqId: str) -> str:
    try:
        return eval(
            requests.get(
                "https://api.oioweb.cn/api/qq/info?qq={}".format(qqId)
            ).content.decode("utf-8")
        )["result"]["nickname"]
    except:
        return qqId


def getMoveEn(moveNameEn: str):
    return moveDataDictEn[moveNameEn]


LevelRange = Annotated[int, Range(1, 100)]
IvRange = Annotated[int, Range(0, 31)]
EvRange = Annotated[int, Range(0, 252)]
statsLevelRange = Annotated[int, Range(-6, 6)]

statList = ["HP", "ATK", "DEF", "SPA", "SPD", "SPE"]


@dataclass
class IVs:
    HP: IvRange = 0
    ATK: IvRange = 0
    DEF: IvRange = 0
    SPA: IvRange = 0
    SPD: IvRange = 0
    SPE: IvRange = 0


@dataclass
class StatsLevel:
    ATK: statsLevelRange = 0
    DEF: statsLevelRange = 0
    SPA: statsLevelRange = 0
    SPD: statsLevelRange = 0
    SPE: statsLevelRange = 0
    ACC: statsLevelRange = 0
    EVA: statsLevelRange = 0


@dataclass
class EVs:
    HP: EvRange = 0
    ATK: EvRange = 0
    DEF: EvRange = 0
    SPA: EvRange = 0
    SPD: EvRange = 0
    SPE: EvRange = 0

    def changeEv(self, ev: str, num: int, addMode: bool = True):
        if ev.upper() not in statList:
            print("Ev not valid!")
            return
        eval("self.{}{}={}".format(ev.upper(), "+" if addMode else "-", num))
