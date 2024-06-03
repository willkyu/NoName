from OlivOS.API import Event

from sim.globalUtils import *
from sim.field import Field


class Battle:
    groupId: str
    turn: int
    field: Field
    playerDict: dict[str:str]  # {qqId: nickname}
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
        self.promoterId = playerId
        self.playerDict[playerId] = getNickname(playerId)
        # self.playerIdList.append(playerId)
        self.battleMode = battleMode
        self.log = []
        self.playerNum = 4 if self.battleMode == "chaos4" else 2
        self.bot.send(
            "group",
            self.groupId,
            "[{}]发出了对战邀请，当前状态：{}/{}".format(
                self.playerDict[playerId], len(self.playerDict), self.playerNum
            ),
        )
        pass

    def addPlayer(self, playerId: str):
        if len(self.playerDict) >= self.playerNum:
            return False
        self.playerDict[playerId] = getNickname(playerId)
        if len(self.playerDict) == self.playerNum:
            self.bot.send(
                "group",
                self.groupId,
                "[{}]接受了对战邀请，当前状态：{}/{}\n即将开始对战...".format(
                    self.playerDict[playerId], len(self.playerDict), self.playerNum
                ),
            )
            self.start()
        else:
            self.bot.send(
                "group",
                self.groupId,
                "[{}]接受了对战邀请，当前状态：{}/{}".format(
                    self.playerDict[playerId], len(self.playerDict), self.playerNum
                ),
            )

    def start(self):
        pass

    def eachTurn(self):
        commandListThisTurn = self.field.calculateCommandOrder()
        for commandTuple in commandListThisTurn:
            self.field.exeCommand(*commandTuple)
        pass

    def end(self):
        pass

    pass
