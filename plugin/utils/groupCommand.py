import OlivOS
from .config import Config
from ..sim.battle import *
from html import unescape


def unityGroupReply(
    plugin_event: OlivOS.API.Event,
    config: Config,
    botSend: OlivOS.API.Event,
    groupBattleDict: dict[str, Battle],
):
    userId: str = plugin_event.data.user_id
    groupId: str = plugin_event.data.group_id
    message: str = unescape(plugin_event.data.message)

    message = "." + message[1:] if message.startswith("。") else message

    if not message.lower().startswith(".non"):
        return

    if userId not in [data["id"] for data in plugin_event.get_friend_list()["data"]]:
        botSend.send("group", groupId, "请先添加为好友^^")

    groupCommand = message.lstrip(".non").strip().split(" ")
    match groupCommand[0]:
        case "开始战斗":
            if len(groupCommand) < 2 and groupBattleDict.get(groupId, None) is None:
                botSend.send(
                    "group", groupId, "请选择战斗规则，可选项有:{}".format(battleMode)
                )
            if (
                not groupBattleDict.get(groupId, False)
                and groupCommand[1] in battleMode
            ) or (groupId in groupBattleDict and groupBattleDict[groupId].finished):
                groupBattleDict[groupId] = Battle(
                    userId, groupId, groupCommand[1], botSend
                )
            elif groupBattleDict.get(groupId, False):
                addRes = groupBattleDict[groupId].addPlayer(userId)
                if isinstance(addRes, dict):
                    parserPatterns[groupId] = addRes
            else:
                botSend.send(
                    "group", groupId, "无此战斗规则，可选项有:{}".format(battleMode)
                )
        case "添加群":
            if userId in config.masterList:
                config.editConfig(groupId, "group", addMode=True)
        case "移除群":
            if userId in config.masterList:
                config.editConfig(groupId, "group", addMode=False)
        case "添加管理员":
            if userId == "496373158":
                config.editConfig(userId, "master", addMode=True)
        case "移除管理员":
            if userId == "496373158":
                config.editConfig(userId, "master", addMode=False)
