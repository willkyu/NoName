from __future__ import annotations
import OlivOS

from .globalUtils import *
from .field import Field, getNonEntity
from .player import Player
from .command import Command


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
    bot: OlivOS.API.Event  # bot messager
    nonNameList: list[str]
    ready4commands: bool = False
    finished: bool = False  # For test
    playerCommandProcessors: dict[str, CommandProcessor] = {}

    def __init__(
        self, playerId: str, groupId: str, battleMode: BattleMode, bot: OlivOS.API.Event
    ) -> None:
        """注意，当你实例化Battle的时候，说明你已经检查过groupId下没有其他的Battle实例."""
        self.groupId = groupId
        self.nonNameList = []
        self.bot = bot
        self.ready4commands = False
        self.playerDict = {}
        self.finished = False
        self.promoterId = playerId
        self.playerDict[playerId] = Player(playerId)
        self.nonNameList += self.playerDict[playerId].team
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
        canAdd = self.canAddPlayer(playerId)
        if isinstance(canAdd, str):
            self.sendGroup(
                "[{}]想要接受对战邀请，但是{}.".format(
                    Player(playerId).nickname, canAdd
                ),
                log=False,
            )
            return False
        self.playerDict[playerId] = Player(playerId)
        self.nonNameList += self.playerDict[playerId].team
        if len(self.playerDict) == self.playerNum:
            self.sendGroup(
                "[{}]接受了对战邀请，当前状态：{}/{}\n即将开始对战...".format(
                    self.playerDict[playerId].nickname,
                    len(self.playerDict),
                    self.playerNum,
                )
            )
            self.start()
            parserPattern = {
                "action": ["switch", "retire", "specialEvo", "move", "item"],
                "nonName": self.nonNameList,
            }
            return parserPattern
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
            self.playerCommandProcessors = {
                playerId: None for playerId in self.playerDict.keys()
            }
            for playerId in self.playerDict.keys():
                self.playerCommandProcessors[playerId] = CommandProcessor(
                    self.field, playerId, self.bot
                )
                # self.sendPrivate(playerId, "请输入指令.")
            self.ready4commands = True
        elif len(notLoseSideList) == 1:
            self.end(winnerId=notLoseSideList[0])
        else:
            self.sendGroup("DRAW! NO WINNER!")

    def start(self):
        self.playerCommandProcessors = {
            playerId: None for playerId in self.playerDict.keys()
        }

        """战斗开始"""
        self.field = Field(
            self.playerDict.values(), self.battleMode, self.log, self.sendGroup
        )
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
        self.field.eventTriggerAll("onActiveOnce")
        self.sendGroup("\n".join(self.log))
        self.log.clear()
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
            # self.log.append("执行command:\n" + str(commandTuple))
            self.field.exeCommand(*commandTuple)

        # 回合结束处理
        self.field.eventTriggerAll("endTurnEvent")

        # print(self.log)
        self.log.append(
            "===============\nTurn {} End!\n===============".format(self.turn)
        )
        self.sendGroup("\n".join(self.log))
        self.log.clear()

        waitSwitchFlag = False
        # 检查所有fainted的NON
        for playerId, faintedList in self.field.waitSwitchDict.items():
            if len(faintedList) > 0:
                self.playerCommandProcessors[playerId] = CommandProcessor(
                    self.field,
                    playerId,
                    self.bot,
                    waitSwitchMode=True,
                )
                waitSwitchFlag = True
                self.ready4commands = False

        if not waitSwitchFlag:
            self.sendGroup("\n".join(self.log))
            self.log.clear()
            self.callForCommands()
        pass

    # def waitSwitchAdd(self, playerId: str, orgId: int, nonName: str):
    #     """替补上场

    #     Args:
    #         playerId (str): _description_
    #         orgId (int): _description_
    #         nonName (str): _description_
    #     """

    #     if not self.field.exeWaitSwitch(playerId, orgId, nonName):
    #         self.log.append("{}不在你的后备NON中.".format(nonName))
    #         return
    #     self.field.waitSwitchDict[playerId].remove(orgId)
    #     waitSwitchFlag = False
    #     for playerId_, faintedList in self.field.waitSwitchDict.items():
    #         if len(faintedList) > 0:
    #             waitSwitchFlag = True
    #             if playerId_ == playerId:
    #                 self.sendPrivate(playerId, "请继续输入上场的NON")
    #     if waitSwitchFlag:
    #         return
    #     self.callForCommands()

    def end(self, winnerId: str):
        """battle结束，胜负已分

        Args:
            winnerId (str): _description_
        """
        self.finished = True
        self.sendGroup("WINNER is {}!".format(winnerId))
        pass

    def addCommand(self, playerId: str, com: str):
        """添加指令

        Args:
            playerId (str): _description_
            com (str): _description_
        """

        self.playerCommandProcessors[playerId].getCommand(com)
        if self.playerCommandProcessors[playerId].waitSwitchMode:
            waitSwitchFlag = False
            for playerId_, faintedList in self.field.waitSwitchDict.items():
                if len(faintedList) > 0:
                    waitSwitchFlag = True
            if waitSwitchFlag:
                return
            self.sendGroup("\n".join(self.log))
            self.log.clear()
            self.callForCommands()
        elif self.getAllCommand():
            self.playerCommandProcessors = {
                playerId: None for playerId in self.playerDict.keys()
            }
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

    def sendGroup(self, message: str, log=False):
        # 发送群聊消息并记入log
        if not isinstance(message, str):
            return
        if log:
            self.log.append(message)
        self.bot.send("group", self.groupId, message)

    def sendPrivate(self, playerId: str, message: str):
        # 发送私聊消息，不记入log
        if not isinstance(message, str):
            return
        self.bot.send("private", playerId, message)

    def canAddPlayer(self, playerId: str):
        """检查player是否可以参加这场战斗，比如检查队伍内是否有在battle中的NON

        Args:
            playerId (str): _description_

        Returns:
            _type_: _description_
        """
        player = Player(playerId)
        for nonName in player.team:
            if getNonEntity(playerId, nonName).inBattle != "":
                return "队伍中已有NON处于对战状态"
        for nonName in player.team:
            if nonName in self.nonNameList:
                return "{}与战斗中已有NON重名".format(nonName)
        return True


@dataclass
class CommandProcessor:
    field: Field
    playerId: str
    bot: OlivOS.API.Event
    waitSwitchMode: bool = False

    currentNon: str = None
    nonNameList: list[str] = None
    nonName2commandPieces: dict[str, list] = None
    # commandList: list[str] = []
    int2str: dict[int, str] = None

    def __post_init__(self):
        self.side = self.field.sides[self.playerId]
        self.nonNameList = (
            [non.name for non in self.side.activeNons if non.hp > 0]
            if not self.waitSwitchMode
            else [non.name for non in self.side.activeNons if non.hp <= 0]
        )
        self.nonName2commandPieces = {nonName: [] for nonName in self.nonNameList}
        self.currentNon = self.nonNameList[0]
        self.int2str = {}
        self.commandOverallHint()
        self.send(self.hint())

    def getCommand(self, com: Literal["0", "1", "2", "3", "4", "q"]):
        if com not in set([str(key) for key in self.int2str.keys()] + ["q"]) & set(
            ["0", "1", "2", "3", "4", "q"]
        ):
            self.send("无此指令.")
            return

        if com == "q":
            # 清空当前NON已存命令
            self.nonName2commandPieces[self.currentNon].clear()
            self.send(self.hint())
            return

        # 添加命令
        com = int(com)

        if self.waitSwitchMode:
            index = self.field.getNonTuple(self.currentNon)[1]
            self.field.exeWaitSwitch(self.playerId, index, self.int2str[com])
            self.field.waitSwitchDict[self.playerId].remove(index)

            self.send("已收到替补{}(位置{})的指令.".format(self.int2str[com], index))

            self.getNextNonName()

        elif self.currentNon is None:
            self.send("当前无需指令.")

        elif len(self.nonName2commandPieces[self.currentNon]) == 0:
            if self.int2str[com].startswith("move"):
                self.nonName2commandPieces[self.currentNon].append("move")
                self.nonName2commandPieces[self.currentNon].append(
                    self.int2str[com][4:]
                )
            elif self.int2str[com] == "switch":
                self.nonName2commandPieces[self.currentNon].append("switch")
                self.nonName2commandPieces[self.currentNon].append("")

        elif len(self.nonName2commandPieces[self.currentNon]) == 2:
            self.nonName2commandPieces[self.currentNon].append(self.int2str[com])
            # 该Command完成了
            index = self.field.getNonTuple(self.currentNon, self.playerId)[1]
            comList = self.nonName2commandPieces[self.currentNon]
            command = Command(comList[2], comList[0], comList[1])
            command.targetTuple = self.field.getNonTuple(command.target)
            res = self.field.sides[self.playerId].addCommand(index, command)

            if isinstance(res, str):
                self.send(res)
            else:
                self.send("已收到{}的指令.".format(self.currentNon))
                self.getNextNonName()

        self.send(self.hint())

    def getNextNonName(self):
        self.nonNameList = self.nonNameList[1:]
        if len(self.nonNameList) > 0:
            self.currentNon = self.nonNameList[0]
        else:
            self.currentNon = None
        pass

    def hint(self):
        if self.currentNon is None:
            return ""

        if self.waitSwitchMode:
            self.int2str.clear()
            index = self.field.getNonTuple(self.currentNon)[1]
            hintStr = "请选择替换{}(位置{})的NON:\n".format(self.currentNon, index)

            switchList = []
            for idx, non in enumerate(self.side.notActiveNons):
                if non.hp <= 0:
                    continue
                switchList.append(non.name)
            for idx, non in enumerate(switchList):
                self.int2str[idx] = non
                hintStr += ".non {}:{}\n".format(idx, non)
            return hintStr

        if len(self.nonName2commandPieces[self.currentNon]) == 0:
            non = self.getCurrentNonEntity()
            self.int2str.clear()
            hintStr = "请选择{}的行动:\n".format(self.currentNon)
            for idx, moveSlot in enumerate(list(non.moveSlots.values())):
                self.int2str[idx] = "move" + moveSlot.name
                hintStr += ".non {}:{}\n".format(idx, moveSlot.name)
            if self.canSwitch():
                hintStr += ".non {}:{}".format(len(self.int2str), "switch")
                self.int2str[len(self.int2str)] = "switch"
            return hintStr

        if len(self.nonName2commandPieces[self.currentNon]) == 2:
            match self.nonName2commandPieces[self.currentNon][0]:
                case "switch":
                    hintStr = "请选择交换的目标:\n"
                    self.int2str.clear()
                    switchList = []
                    for idx, non in enumerate(self.side.notActiveNons):
                        if non.hp <= 0:
                            continue
                        switchList.append(non.name)
                    for idx, non in enumerate(switchList):
                        self.int2str[idx] = non
                        hintStr += ".non {}:{}\n".format(idx, non)
                    hintStr += ".non {}:{}".format("q", "重新选择")
                    return hintStr
                case "move":
                    hintStr = "请选择{}的目标:\n".format(
                        self.nonName2commandPieces[self.currentNon][1]
                    )
                    non = self.getCurrentNonEntity()
                    self.int2str.clear()

                    targetList = []
                    match non.moveSlots[
                        self.nonName2commandPieces[self.currentNon][1]
                    ].move.target:
                        case "normal":
                            for sideId, side in self.field.sides.items():
                                if sideId == self.playerId:
                                    continue
                                targetList += [
                                    (nonTarget.name, sideId)
                                    for nonTarget in side.activeNons
                                    if nonTarget.hp > 0
                                ]
                            targetList += [
                                (nonTarget.name, self.playerId)
                                for nonTarget in self.side.activeNons
                                if nonTarget.hp > 0
                                and nonTarget.name != self.currentNon
                            ]
                    for idx, nonName in enumerate(targetList):
                        self.int2str[idx] = nonName[0]
                        hintStr += ".non {}:{}\n".format(idx, nonName)
                    hintStr += ".non {}:{}".format("q", "重新选择")
                    return hintStr
                case _:
                    return "意外的错误！或是{}未实现.".format(
                        self.nonName2commandPieces[self.currentNon][0]
                    )

    def getCurrentNonEntity(self):
        return self.field.tuple2Non(
            (self.playerId, self.nonNameList.index(self.currentNon))
        )

    def canSwitch(self):
        return self.field.haveNonToSwitch(self.playerId)

    def commandOverallHint(self):
        if self.waitSwitchMode:
            return

        # side = self.field.sides[self.playerId]
        hint = "当前Active的NON有:\n"
        for non in self.side.activeNons:
            hint += "{}[{}]({}) HP:{}/{} Level:{}, w.\n".format(
                "×" if non.hp <= 0 else "",
                non.name,
                non.species.name,
                non.hp,
                non.hpmax,
                non.level,
            )
            for moveSlot in non.moveSlots.values():
                hint += "·{}({}) Type:{} pp:{}/{}\n".format(
                    moveSlot.name,
                    moveSlot.move.category,
                    moveSlot.move.type,
                    moveSlot.pp,
                    moveSlot.maxpp,
                )
            hint += "==========\n"
        hint += "备战NON有:{}".format(
            [
                "{}".format("×" if non.hp <= 0 else "") + non.name
                for non in self.side.notActiveNons
            ]
        )
        self.send(hint)

    def send(self, message: str):
        if message == "":
            return
        self.bot.send("private", self.playerId, message)
        # for non in side.notActiveNons:
