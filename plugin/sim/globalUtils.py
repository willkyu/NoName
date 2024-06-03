from dataclasses import dataclass
from typing import Literal, Callable, Annotated
from configparser import ConfigParser
from json import dump, load
import os
from species import SpeciesData

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



def getSpeciesBuffResult(species:SpeciesData, area: str):
    if not species.liveArea.__contains__(area):
        return 0
    timePeriodRateBuff = getTimePeriodRateBuff()
    seasonRateBuff = getSeasonRateBuff()
    if timePeriodRateBuff == 0 or seasonRateBuff == 0:
        return 0
    return species.baseRateBuff + timePeriodRateBuff + seasonRateBuff

def getTimePeriodRateBuff(species:SpeciesData):
    now = datetime.datetime.now().hour
    if 5 <= now < 10:
        return species.morningRateBuff
    elif 10 <= now < 14:
        return species.noonRateBuff
    elif 14 <= now < 17:
        return species.afternoonRateBuff
    elif 17 <= now <= 24 or 0 <= now < 5:
        return species.nightRateBuff

def getSeasonRateBuff(species:SpeciesData):
    now = datetime.datetime.today().month
    if 3 <= now < 6:
        return species.springRateBuff
    elif 6 <= now < 9:
        return species.summerRateBuff
    elif 9 <= now < 12:
        return species.autumnRateBuff
    elif now == 12 or now == 1 or now == 2:
        return species.winterRateBuff
