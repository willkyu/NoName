from OlivOS.API import Event

from sim.globalUtils import *
from sim.field import Field
from sim.player import Player


class Battle:
    groupId: str
    turn: int
    field: Field
    playerDict: dict[str, Player]  # {qqId: Player}
    promoterId: str  # 发起人
    battleMode: BattleMode
    log: list[str]
    playerNum: int
    bot: Event  # bot messager

    def __init__(
        self, playerId: str, groupId: str, battleMode: BattleMode, bot: Event
    ) -> None:
        """注意，当你实例化Battle的时候，说明你已经检查过groupId下没有其他的Battle实例."""
        self.groupId = groupId
        self.bot = bot
        self.playerDict = {}
        self.promoterId = playerId
        self.playerDict[playerId] = Player(playerId)
        # self.playerIdList.append(playerId)
        self.battleMode = battleMode
        self.log = []
        self.playerNum = 4 if self.battleMode == "chaos4" else 2
        self.sendAndLog(
            "[{}]发出了对战邀请，当前状态：{}/{}".format(
                self.playerDict[playerId].nickname, len(self.playerDict), self.playerNum
            )
        )
        pass

    def addPlayer(self, playerId: str):
        if len(self.playerDict) >= self.playerNum:
            return False
        self.playerDict[playerId] = getNickname(playerId)
        if len(self.playerDict) == self.playerNum:
            self.sendAndLog(
                "[{}]接受了对战邀请，当前状态：{}/{}\n即将开始对战...".format(
                    self.playerDict[playerId], len(self.playerDict), self.playerNum
                )
            )
            self.start()
        else:
            self.sendAndLog(
                "[{}]接受了对战邀请，当前状态：{}/{}".format(
                    self.playerDict[playerId], len(self.playerDict), self.playerNum
                )
            )

    def start(self):
        self.field = Field(self.playerDict.values(), self.battleMode)
        startBattleMessage = "————————————\n▼ 战斗开始！\n┣———————————\n"
        for playerId in self.playerDict.keys():
            startBattleMessage += "▶ 玩家[{}]派出了[{}]({}){}\n".format(
                self.playerDict[playerId].nickname,
                self.field.sides[playerId].activeNons[0].name,
                self.field.sides[playerId].activeNons[0].species.name,
                (
                    ""
                    if self.battleMode != "double"
                    else "与[{}]({})".format(
                        self.field.sides[playerId].activeNons[1].name,
                        self.field.sides[playerId].activeNons[1].species.name,
                    )
                ),
            )
        startBattleMessage += "————————————"
        self.sendAndLog(startBattleMessage)
        pass

    def eachTurn(self):
        self.turn += 1
        commandListThisTurn = self.field.calculateCommandOrder()
        for commandTuple in commandListThisTurn:
            self.field.exeCommand(*commandTuple)
        pass

    def end(self):
        pass

    pass

    def sendAndLog(self, message: str):
        # 发送群聊消息并记入log
        if not isinstance(message, str):
            return
        self.log.append(message)
        self.bot.send("group", self.groupId, message),

    def sendPrivate(self, playId: str, message: str):
        # 发送私聊消息，不记入log
        if not isinstance(message, str):
            return
        self.bot.send("private", playId, message),
