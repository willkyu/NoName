from OlivOS.API import Event

from sim.globalUtils import *
from sim.field import Field, getNonEntity
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
        self.sendGroup(
            "[{}]发出了对战邀请，当前状态：{}/{}".format(
                self.playerDict[playerId].nickname, len(self.playerDict), self.playerNum
            )
        )
        pass

    def addPlayer(self, playerId: str):
        """添加玩家，成功True，失败False

        Args:
            playerId (str): _description_

        Returns:
            _type_: _description_
        """
        if len(self.playerDict) >= self.playerNum:
            return False
        if not Battle.canAddPlayer(playerId):
            self.sendGroup(
                "[{}]想要接受对战邀请，但是队伍中已有NON处于对战状态.", log=False
            )
            return False
        self.playerDict[playerId] = getNickname(playerId)
        if len(self.playerDict) == self.playerNum:
            self.sendGroup(
                "[{}]接受了对战邀请，当前状态：{}/{}\n即将开始对战...".format(
                    self.playerDict[playerId], len(self.playerDict), self.playerNum
                )
            )
            self.start()
        else:
            self.sendGroup(
                "[{}]接受了对战邀请，当前状态：{}/{}".format(
                    self.playerDict[playerId], len(self.playerDict), self.playerNum
                )
            )
        return True

    def start(self):
        self.field = Field(self.playerDict.values(), self.battleMode, self.log)
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
        for player in self.playerDict.keys():
            for non in self.field.sides[player].activeNons:
                non.inBattle = self.groupId
                non.save()
            for non in self.field.sides[player].notActiveNons:
                non.inBattle = self.groupId
                non.save()

    def eachTurn(self):
        self.turn += 1
        commandListThisTurn = self.field.calculateCommandOrder()
        for commandTuple in commandListThisTurn:
            self.field.exeCommand(*commandTuple)
        pass

    def end(self):
        pass

    pass

    def sendGroup(self, message: str, log=True):
        # 发送群聊消息并记入log
        if not isinstance(message, str):
            return
        if log:
            self.log.append(message)
        self.bot.send("group", self.groupId, message)

    def sendPrivate(self, playId: str, message: str):
        # 发送私聊消息，不记入log
        if not isinstance(message, str):
            return
        self.bot.send("private", playId, message)

    @staticmethod
    def canAddPlayer(playerId: str):
        for nonName in Player(playerId).team:
            if getNonEntity(playerId, nonName).inBattle != "":
                return False
        return True
