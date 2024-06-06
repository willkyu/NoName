from OlivOS.API import Event

from sim.globalUtils import *
from sim.field import Field, getNonEntity
from sim.player import Player


class log(list):
    def append(self, object: object) -> None:
        print(str(object))
        return super().append(object)


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
        self.log = log()
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
                "[{}]想要接受对战邀请，但是队伍中已有NON处于对战状态.".format(
                    self.playerDict[playerId].nickname
                ),
                log=False,
            )
            return False
        self.playerDict[playerId] = Player(playerId)
        if len(self.playerDict) == self.playerNum:
            self.sendGroup(
                "[{}]接受了对战邀请，当前状态：{}/{}\n即将开始对战...".format(
                    self.playerDict[playerId].nickname,
                    len(self.playerDict),
                    self.playerNum,
                )
            )
            self.start()
        else:
            self.sendGroup(
                "[{}]接受了对战邀请，当前状态：{}/{}".format(
                    self.playerDict[playerId].nickname,
                    len(self.playerDict),
                    self.playerNum,
                )
            )
        return True

    def callForCommands(self):
        """首先检查是否决出胜负，否则向所有玩家发送 请输入指令"""
        notLoseSideList = [
            sideId for sideId, side in self.field.sides.items() if not side.lose
        ]
        if len(notLoseSideList) > 1:
            for playerId in self.playerDict.keys():
                self.sendPrivate(playerId, "请输入指令.")
        elif len(notLoseSideList) == 1:
            self.end(winnerId=notLoseSideList[0])
        else:
            self.sendGroup("DRAW! NO WINNER!")

    def start(self):
        """战斗开始"""
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
        # for player in self.playerDict.keys():
        #     for non in self.field.sides[player].activeNons:
        #         non.inBattle = self.groupId
        #         non.save()
        #     for non in self.field.sides[player].notActiveNons:
        #         non.inBattle = self.groupId
        #         non.save()
        self.sendGroup(startBattleMessage)
        self.turn = 0
        self.callForCommands()

    def eachTurn(self):
        """每回合的操作"""
        self.turn += 1
        self.sendGroup(
            "===============\nTurn {} Start!\n===============".format(self.turn)
        )
        commandListThisTurn = self.field.calculateCommandOrder()
        for commandTuple in commandListThisTurn:
            self.log.append("执行command:\n" + str(commandTuple))
            self.field.exeCommand(*commandTuple)

        # 回合结束处理
        self.field.eventTriggerAll("endTurnEvent")

        waitSwitchFlag = False
        # 检查所有fainted的NON
        for playerId, faintedList in self.field.waitSwitchDict.items():
            if len(faintedList) > 0:
                self.sendPrivate(playerId, "请输入上场的NON")
                waitSwitchFlag = True

        if not waitSwitchFlag:
            self.callForCommands()
        pass

    def waitSwitchAdd(self, playerId: str, orgId: int, nonName: str):
        """替补上场

        Args:
            playerId (str): _description_
            orgId (int): _description_
            nonName (str): _description_
        """

        if not self.field.exeWaitSwitch(playerId, orgId, nonName):
            self.log.append("{}不在你的后备NON中.".format(nonName))
            return
        self.field.waitSwitchDict[playerId].remove(orgId)
        waitSwitchFlag = False
        for playerId_, faintedList in self.field.waitSwitchDict.items():
            if len(faintedList) > 0:
                waitSwitchFlag = True
                if playerId_ == playerId:
                    self.sendPrivate(playerId, "请继续输入上场的NON")
        if waitSwitchFlag:
            return
        self.callForCommands()

    def end(self, winnerId: str):
        """battle结束，胜负已分

        Args:
            winnerId (str): _description_
        """
        self.sendGroup("WINNER is {}!".format(winnerId))
        pass

    def addCommand(self, playerId: str, nonName: str, command):
        """添加指令

        Args:
            playerId (str): _description_
            nonName (str): _description_
            command (_type_): _description_
        """

        index = self.field.getNonTuple(nonName, playerId)[1]
        if self.field.tuple2Non((playerId, index), active=True).name != nonName:
            self.sendPrivate(
                playerId, "============\n{}没有active.\n==============".format(nonName)
            )
            return

        res = self.field.sides[playerId].addCommand(index, command)

        if isinstance(res, str):
            self.sendPrivate(playerId, res)
            return

        # * 这里很重要，之后的command建议都只使用targetTuple来定位target，而不是直接用target
        command = self.field.sides[playerId].commandDict[index]
        command.targetTuple = self.field.getNonTuple(command.target)
        if self.getAllCommand():
            for commandTupele in self.field.calculateCommandOrder():
                command = self.field.sides[commandTupele[0]].commandDict[
                    commandTupele[1]
                ]
                targetTuple = self.field.getNonTuple(command.target)
                self.sendGroup(
                    "· 玩家[{}]的[{}]准备对玩家[{}]的[{}]使用[{}].".format(
                        commandTupele[0],
                        self.field.tuple2Non(commandTupele).name,
                        targetTuple[0],
                        self.field.tuple2Non(targetTuple).name,
                        command.move,
                    )
                )
            self.eachTurn()

    def getAllCommand(self) -> bool:
        """检查是否收到所有指令

        Returns:
            bool: _description_
        """
        for side in self.field.sides.values():
            if not side.getAllCommand():
                return False
        return True

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
        """检查player是否可以参加这场战斗，比如检查队伍内是否有在battle中的NON

        Args:
            playerId (str): _description_

        Returns:
            _type_: _description_
        """
        for nonName in Player(playerId).team:
            if getNonEntity(playerId, nonName).inBattle != "":
                return False
        return True
