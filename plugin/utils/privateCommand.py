import OlivOS
from html import unescape
from .config import Config
from ..sim.battle import *
import re


def parser(message: str, parserPattern: dict[str, list[str]]):
    resDict = {"nonName": None, "action": None, "target": None, "move": ""}
    try:
        target = re.search("[对与和跟]\[(.*?)\]", message).group(1)
    except:
        return "没有匹配到target"
    if target not in parserPattern["nonName"]:
        return "没有{}这个NON".format(target)
    resDict["target"] = target
    findAllRes = re.findall("[^对与和跟]\[(.*?)\]", message) + re.findall(
        "^\[(.*?)\]", message
    )
    if len(findAllRes) < 2 or len(findAllRes) > 3:
        return "指令缺失"
    for item in findAllRes:
        if item in parserPattern["action"]:
            resDict["action"] = item
        elif item in parserPattern["nonName"]:
            resDict["nonName"] = item
        else:
            resDict["move"] = item
    if None in resDict.values():
        return "指令缺失"
    return resDict


def parserSwitch(message: str, parserPattern: dict[str, list[str]]):
    resDict = {"orgId": None, "nonName": None}
    try:
        target = re.findall("(\d).*\[(.*?)\]", message)[0]
        resDict["orgId"], resDict["nonName"] = target
    except:
        try:
            target = re.findall("\[(.*?)\].*(\d)", message)[0]
            resDict["nonName"], resDict["orgId"] = target
        except:
            return False
    if resDict["nonName"] not in parserPattern["nonName"]:
        return False
    resDict["orgId"] = int(resDict["orgId"])
    return resDict


def unityPrivateReply(
    plugin_event: OlivOS.API.Event,
    config: Config,
    botSend: OlivOS.API.Event,
    parserPatterns: dict[str, dict[str, list[str]]],
    groupBattleDict: dict[str, Battle],
):
    userId: str = plugin_event.data.user_id
    # groupId: str = plugin_event.data.group_id
    message: str = unescape(plugin_event.data.message)

    if not message.lower().startswith(".non"):
        return

    groupId = False
    for groupId_ in groupBattleDict:
        if userId in groupBattleDict[groupId_].playerDict:
            groupId = groupId_
            break
    # if not groupId:
    #     botSend.send("private", userId, "你未参加任何战斗.")
    #     return

    userCommand = message.lstrip(".non").strip()
    if groupBattleDict[groupId].ready4commands:
        parserRes = parser(message, parserPatterns[groupId])
        if isinstance(parserRes, dict):
            groupBattleDict[groupId].addCommand(
                userId,
                parserRes["nonName"],
                Command(parserRes["target"], parserRes["action"], parserRes["move"]),
            )
        else:
            botSend.send(
                "private",
                userId,
                "指令有误:{}！注意，指令中【与、对、和、跟】只能紧跟target.".format(
                    parserRes
                ),
            )
    elif len(groupBattleDict[groupId].field.waitSwitchDict[userId]) > 0:
        parserRes = parserSwitch(message, parserPatterns[groupId])
        groupBattleDict[groupId].waitSwitchAdd(userId, **parserRes)
    else:
        botSend.send("private", userId, "没有这条指令.")
