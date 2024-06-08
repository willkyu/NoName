import OlivOS
from html import unescape
from .config import Config
from ..sim.battle import *
import re


def unityPrivateReply(
    plugin_event: OlivOS.API.Event,
    config: Config,
    botSend: OlivOS.API.Event,
    groupBattleDict: dict[str, Battle],
):
    userId: str = plugin_event.data.user_id
    # groupId: str = plugin_event.data.group_id
    message: str = unescape(plugin_event.data.message)

    message = "." + message[1:] if message.startswith("。") else message

    if not message.lower().startswith(".non"):
        return

    groupId = False
    for groupId_ in groupBattleDict:
        if userId in groupBattleDict[groupId_].player_dict:
            groupId = groupId_
            break
    if not groupId:
        botSend.send("private", userId, "你未参加任何战斗.")
        return

    userCommand = message[4:].strip()
    if userCommand in ["0", "1", "2", "3", "4", "q"]:
        if userId in groupBattleDict[groupId].player_command_processors.keys():
            groupBattleDict[groupId].add_command(userId, userCommand)
        else:
            botSend.send("private", userId, "无需发出指令.")

        # elif len(groupBattleDict[groupId].field.waitSwitchDict[userId]) > 0:
        #     if (
        #         len(groupBattleDict[groupId].field.waitSwitchDict[userId]) == 1
        #     ):  # 只需要换一个上场
        #         orgId = groupBattleDict[groupId].field.waitSwitchDict[userId][0]
        #         parserRes = parserSwitch(message, parserPatterns[groupId])
        #         if isinstance(parserRes, dict):
        #             parserRes["orgId"] = orgId
        #             groupBattleDict[groupId].waitSwitchAdd(userId, **parserRes)
        #         else:
        #             botSend.send(
        #                 "private",
        #                 userId,
        #                 "指令有误！NON请用中括号括起来！".format(parserRes),
        #             )
        #         return

        #     parserRes = parserSwitch(message, parserPatterns[groupId], single=False)
        #     groupBattleDict[groupId].waitSwitchAdd(userId, **parserRes)
    else:
        botSend.send("private", userId, "没有这条指令.")
