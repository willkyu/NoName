from OlivOS.API import Event, Proc_templet
from config import Config
from plugin.sim.battle import Battle


def unity_group_reply(
    plugin_event: Event, Proc: Proc_templet, config: Config, botSend: function
) -> None:
    groupID: str
    message: str
    userID: str

    groupID = plugin_event.data.group_id
    message = plugin_event.data.message
    userID = plugin_event.data.user_id
    userName = plugin_event.data.user_name
    if groupID not in config.groupList or message.lower().startswith(".non"):
        return
    message = message[4:].lower()
    if message.startswith("battle"):
        # start a battle
        if groupID not in config.battleGroupDict:
            config.battleList.append(Battle(groupID, botSend))
            config.battleGroupDict[groupID] = len(config.battleList) - 1
            config.battlePlayerDict[userID] = len(config.battleList) - 1
            botSend("用户【{}】开启了一场NON对战\n当前状态：1/2".format(userName))
            config.battleList[config.battleGroupDict[groupID]].addPlayer(userID)
        elif len(config.battleList[config.battleGroupDict[groupID]].playerDict) > 1:
            botSend("对战人数已满，请等待结束")
        else:
            config.battlePlayerDict[userID] = config.battleGroupDict[groupID]
            config.battleList[config.battleGroupDict[groupID]].addPlayer(userID)
        pass
    elif message.startswith("draw"):
        # get a monster
        pass
    else:
        # no this command
        plugin_event.reply("Command Error.")

    pass
