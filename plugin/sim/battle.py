import re

from sim.nonClass import NONBattleEntity
from sim.globalTypes import *
from sim.dexFormat import Format


def extractChannelMessages(message, channelIds):
    channelIdSet = set(channelIds)
    channelMessages: ChannelMessages = {
        -1: [],
        0: [],
        1: [],
        2: [],
        3: [],
        4: [],
    }

    for lineMatch, playerMatch, secretMessage, sharedMessage in re.findall(
        splitRegex, message
    ):
        player = int(playerMatch) if playerMatch else 0
        for channelId in channelIdSet:
            line = lineMatch
            if player:
                line = (
                    secretMessage
                    if channelId == -1 or player == channelId
                    else sharedMessage
                )
                if not line:
                    continue
            channelMessages[channelId].append(line)

    return channelMessages


class BattleOptions:
    format_: Format | None
    formatid: ID

    send: function | None
    prng: PRNG | None
    seed: PRNGSeed | None
    rated: bool | str | None
    p1: PlayerOptions | None
    p2: PlayerOptions | None
    p3: PlayerOptions | None
    p4: PlayerOptions | None

    pass


class Battle(BattleOptions):
    pass
