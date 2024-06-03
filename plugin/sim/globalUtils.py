from dataclasses import dataclass
from typing import Literal, Callable, Annotated
from configparser import ConfigParser
from json import dump, load
import os
import requests


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
