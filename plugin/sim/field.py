from random import shuffle, choice
import math

from .globalUtils import *
from .non import NON, MoveSlot
from .command import Command
from .player import Player
from .nonEvents import NonEventsObj


class Side:
    """每一个玩家是一个Side

    Returns:
        _type_: _description_
    """

    nonNum: Literal[1, 2]  # 该规则下一次能出战几个NON
    activeNons: list[NON]  # 出战的NON
    notActiveNons: list[NON]  # 备战NON

    commandDict: dict[int, Command]  # {index, Command} index是出战NON的index

    # 一些其他的东西，如护盾
    shield: bool = False  # 己方全体护盾

    lose = False

    def __init__(self, team: list[NON], battleMode: BattleMode) -> None:
        """给玩家的teamlist，战斗规则

        Args:
            team (list[NON]): _description_
            battleMode (BattleMode): _description_
        """
        self.nonNum = 2 if battleMode == "double" else 1
        self.activeNons, self.notActiveNons = team[: self.nonNum], team[self.nonNum :]
        self.commandDict = {i: None for i in range(self.nonNum)}

    def addCommand(self, index: int, command: Command) -> str | bool:
        """添加指令，如果成功返回True，否则是str，描述不合法原因

        Args:
            index (int): 指令的位置（哪个NON进行操作）
            command (Command): _description_

        Returns:
            str|bool: _description_
        """
        if index >= self.nonNum or index < 0:
            return "指令对象超出范围"
        valid = self.checkCommandValid(index, command)
        if isinstance(valid, str):
            return valid

        # 这里添加其他可能性

        pass
        self.commandDict[index] = command
        # print("{}已添加:\n{}\n".format(index, command))
        return True

    def checkCommandValid(self, index: int, command: Command) -> str | bool:
        """检查指令合法性，如果合法返回True，否则是str，描述不合法原因

        Args:
            index (int): 指令的位置（哪个NON进行操作）
            command (Command): _description_

        Returns:
            str|bool: _description_
        """
        if command.action == "move" and command.move not in [
            moveslot for moveslot in self.activeNons[index].moveSlots.keys()
        ]:
            return "无法使用该NON不会的招式"
        if self.activeNons[index].hp <= 0:
            return "该NON已昏厥"
        # 这之后可以再加别的检查合法性，比如不能交换状态进行交换
        return True

    def calculateNonSpeed(self, commandIndex: int) -> int:
        # 计算指令的NON的当前速度
        non = self.activeNons[commandIndex]
        return non.stat.SPE
        pass

    def getAllCommand(self) -> bool:
        """是否该Side的指令全部收到

        Returns:
            bool: _description_
        """

        if None in [
            self.commandDict[idx]
            for idx, non in enumerate(self.activeNons)
            if non.hp > 0
        ]:
            return False
        return True

    def checkLose(self):
        for non in self.activeNons:
            if non.hp > 0:
                return False
        self.lose = True
        return True

    pass


class Field:
    """包含战斗的各种信息

    Returns:
        _type_: _description_
    """

    sides: dict[str, Side]  # {userId: Side} 有哪几个玩家，分别对应一个Side
    nonTeamDict: dict[str, list[NON]]  # {userId:[NON]} 玩家的队伍
    log: list[str]
    waitSwitchDict: dict[str, list[int]] = (
        None  # 用于存储是否需要等待用户换上NON，一般用于NON fainted之后，有些特殊技能也会用上
    )

    weather: str = "Normal"

    # 一些其他的东西
    lastUsedMove: str | None = None

    pass

    def __init__(
        self,
        playerList: Annotated[list[Player], "len should be 2 or 4"],
        battleMode: BattleMode,
        log: list[str],
    ) -> None:
        """初始化field

        Args:
            playerList (Annotated[list[Player], &quot;len should be 2 or 4&quot;]): 玩家id列表
            battleMode (BattleMode): 规则
            log (list[str]): log
        """
        self.nonTeamDict = {
            player.id: [getNonEntity(player.id, non) for non in player.team]
            for player in playerList
        }
        self.sides = {
            player.id: Side(self.nonTeamDict[player.id], battleMode)
            for player in playerList
        }
        self.log = log

        self.waitSwitchDict = {playerId: [] for playerId in self.sides.keys()}
        pass

    def exeCommand(self, sideId: str, commandIndex: int):
        # * 注意，exeCommand之前必须确保指令可行，也就是在addCommand阶段就要检查指令可行性
        # * 执行指令，sideId与playerId是一个东西
        # do this command
        command: Command = self.sides[sideId].commandDict[commandIndex]

        if self.tuple2Non((sideId, commandIndex)).hp <= 0:
            self.sides[sideId].commandDict[commandIndex] = None
            return

        match command.action:
            case "retire":
                # sideId输
                pass
            case "switch":
                targetNonIndex = command.targetTuple[1]
                self.eventTriggerSingle("beforeSwitch", (sideId, commandIndex))
                self.log.append(
                    "{}收回了{}，派出了{}.".format(
                        sideId,
                        self.sides[sideId].activeNons[commandIndex].name,
                        command.target,
                    )
                )

                # 交换
                (
                    self.sides[sideId].activeNons[commandIndex],
                    self.sides[sideId].notActiveNons[targetNonIndex],
                ) = (
                    self.sides[sideId].notActiveNons[targetNonIndex],
                    self.sides[sideId].activeNons[commandIndex],
                )
                self.eventTriggerSingle("onActiveOnce", (sideId, commandIndex))
            case "specialEvo":
                pass
            case "item":
                pass
            case "move":
                self.exeMove(sideId, commandIndex)
                pass
        self.sides[sideId].commandDict[commandIndex] = None
        pass
        # print(self.log)

    def exeWaitSwitch(self, playerId: str, orgId: int, nonName: str):
        # 执行替补，一般是因为位置空了需要进行备战替补
        # orgId是需要换上的位置index，nonName是换上的NON的name

        if nonName not in [non.name for non in self.sides[playerId].notActiveNons]:
            return False
        targetNonIndex = self.getNonTuple(nonName, playerId)[1]
        # self.eventTriggerSingle("beforeSwitch", (sideId, commandIndex))
        self.log.append(
            "{}派出了{}到位置{}.".format(
                playerId,
                self.sides[playerId].notActiveNons[targetNonIndex].name,
                orgId,
            )
        )
        (
            self.sides[playerId].activeNons[orgId],
            self.sides[playerId].notActiveNons[targetNonIndex],
        ) = (
            self.sides[playerId].notActiveNons[targetNonIndex],
            self.sides[playerId].activeNons[orgId],
        )
        self.eventTriggerSingle("onActiveOnce", (playerId, orgId))
        return True

    def exeMove(self, sideId: str, commandIndex: int):
        # 执行move，比较复杂。还没写完
        command: Command = self.sides[sideId].commandDict[commandIndex]
        if command is None:
            return
        non = self.tuple2Non((sideId, commandIndex))
        non.moveSlots[command.move].pp -= 1
        targetTuple = command.targetTuple
        targetNon = self.tuple2Non(targetTuple)
        if targetNon.hp <= 0:
            targetTuple = self.getRandomActiveNonTuple(targetTuple[0])
            if not targetTuple:
                self.log.append("没有目标.")
                return
            targetNon = self.tuple2Non(targetTuple)
        if non.moveSlots[command.move].move.category != "Auxiliary":
            damage = self.calculateDamage(
                non,
                non.moveSlots[command.move],
                targetNon,
            )
            # self.log.append(
            #     "{}被{}使用{}攻击，受到了{}点伤害，还剩{}HP.".format(
            #         targetNon.name,
            #         non.name,
            #         command.move,
            #         damage,
            #         targetNon.hp - damage,
            #     )
            # )
            self.log.append(
                "{}--[{}]-->{}[HP:{}-{}={}/{}]".format(
                    non.name,
                    command.move,
                    targetNon.name,
                    targetNon.hp,
                    damage,
                    max(targetNon.hp - damage, 0),
                    targetNon.hpmax,
                )
            )
            self.makeDamage(targetTuple, damage)
        else:
            # 辅助招式
            pass

        pass

    def makeDamage(self, nonTuple: tuple[str, int], damage: int):
        nonEntity = self.tuple2Non(nonTuple)
        if nonEntity.hp <= 0:
            return
        nonEntity.hp -= min(damage, nonEntity.hp)
        if nonEntity.hp <= 0:
            self.faintedProcess(nonTuple)

    def getRandomActiveNonTuple(self, sideId=None):
        """获取一个随机的active的NON，不给sideId就从全局active的NON中选。
           现在有个问题是可能会选择自己

        Args:
            sideId (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        tupleList = []
        if sideId is not None:
            for idx in range(self.sides[sideId].nonNum):
                if self.tuple2Non((sideId, idx), active=True).hp > 0:
                    tupleList.append((sideId, idx))
        else:
            for sideId, side in self.sides.items():
                for idx in range(side.nonNum):
                    if self.tuple2Non((sideId, idx), active=True).hp > 0:
                        tupleList.append((sideId, idx))
        if len(tupleList) > 0:
            return choice(tupleList)
        return False

    def faintedProcess(self, targetTuple: tuple[str, int]):
        # fainted的处理
        self.log.append(
            "[{}]的[{}]倒下了……".format(
                getNickname(targetTuple[0]), self.tuple2Non(targetTuple).name
            )
        )
        if self.haveNonToSwitch(targetTuple[0]):
            self.waitSwitchDict[targetTuple[0]].append(targetTuple[1])
            self.log.append("{}将要选择NON到位置{}上.".format(*targetTuple))
        elif self.sides[targetTuple[0]].checkLose():
            self.log.append("{}没有可以拿出的NON了……".format(targetTuple[0]))
        pass

    def calculateDamage(self, orgNon: NON, move: MoveSlot, targetNon: NON):
        # 计算伤害，orgNon是攻击方
        multiply = 1.0 * (1.5 if move.move.type in orgNon.types else 1.0)
        category = move.move.category
        # TODO 计算属性克制倍率
        damage = multiply * (
            (2 * orgNon.level + 10)
            / 250
            * (
                orgNon.stat.ATK
                * (
                    (2 + orgNon.statsLevel.ATK) / 2
                    if orgNon.statsLevel.ATK > 0
                    else 2 / (2 - orgNon.statsLevel.ATK)
                )
                if category == "Physical"
                else (
                    orgNon.stat.SPA * (2 + orgNon.statsLevel.SPA) / 2
                    if orgNon.statsLevel.SPA > 0
                    else 2 / (2 - orgNon.statsLevel.SPA)
                )
            )
            / (
                targetNon.stat.DEF
                * (
                    (2 + orgNon.statsLevel.DEF) / 2
                    if orgNon.statsLevel.DEF > 0
                    else 2 / (2 - orgNon.statsLevel.DEF)
                )
                if category == "Physical"
                else targetNon.stat.SPD
                * (
                    (2 + orgNon.statsLevel.SPD) / 2
                    if orgNon.statsLevel.SPD > 0
                    else 2 / (2 - orgNon.statsLevel.SPD)
                )
            )
            * move.move.basePower
            + 2
        )

        return max(math.floor(damage), 1)

    def calculateCommandOrder(self):
        # 计算指令的顺序，同优先级下速度快的优先
        commandDict: dict[tuple[str, int], Command] = {}

        # 使用shuffle打乱顺序，实现相同速度下的随机排序
        # * 这样做不太对，需要重写
        shuffledSideList = list(self.sides.items())
        shuffle(shuffledSideList)

        for sideId, side in shuffledSideList:
            for commandIndex, command in side.commandDict.items():
                if command != None:
                    commandDict[(sideId, commandIndex)] = command

        # calculate the order
        self.updateCommandPriority(commandDict)
        commandPriorityDict = {
            commandTuple: (
                command.priority if command is not None else 0,
                self.sides[commandTuple[0]].calculateNonSpeed(commandTuple[1]),
            )
            for commandTuple, command in commandDict.items()
        }

        return [
            key
            for key, value in sorted(
                list(commandPriorityDict.items()), key=lambda x: (-x[1][0], -x[1][1])
            )
        ]

    def calculateSpeedOrder(self, returnNonEntity=False):
        # 计算指令的速度
        nonSpeedDict: dict[tuple[str, int], NON] = {}

        # 使用shuffle打乱顺序，实现相同速度下的随机排序，需要重写

        shuffledSideList = list(self.sides.items())
        shuffle(shuffledSideList)

        for sideId, side in shuffledSideList:
            for nonIdx in range(len(side.activeNons)):
                if self.tuple2Non((sideId, nonIdx)).hp > 0:
                    nonSpeedDict[(sideId, nonIdx)] = side.calculateNonSpeed(nonIdx)

        returnList = [
            key for key in sorted(nonSpeedDict.keys(), key=lambda x: (-nonSpeedDict[x]))
        ]
        if returnNonEntity:
            newreturnList = [self.tuple2Non(nonTuple) for nonTuple in returnList]
            return [[returnList[i], newreturnList[i]] for i in range(len(returnList))]
        return returnList

    def updateCommandPriority(
        self, commandDict: dict[tuple[str, int], Command]
    ) -> None:
        # 特殊情况下的优先级更新，比如追击
        pass

    def eventTriggerAll(self, eventName: str, **kwargs):
        # 触发场上所有NON的名为eventName的nonEvent
        if not hasattr(NonEventsObj, eventName):
            return
        for nonTuple, non in self.calculateSpeedOrder(returnNonEntity=True):
            kwargs.update({"org": nonTuple})
            eval("non.nonEvents.{}.exe(self,**kwargs)".format(eventName))

    def eventTriggerSingle(self, eventName: str, nonTuple: tuple[str, int], **kwargs):
        # 触发指定NON的名为eventName的nonEvent
        if not hasattr(NonEventsObj, eventName):
            return
        non = self.tuple2Non(nonTuple)
        kwargs.update({"org": nonTuple})
        eval("non.nonEvents.{}.exe(self,**kwargs)".format(eventName))

    def getNonTuple(self, nonName: str, sideId: str = None):
        """给定一个non的名字，获取他的tuple。tuple可以理解为是该non的定位符。

        Args:
            nonName (str): _description_
            sideId (str, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        if sideId == None:
            for sideId, side in self.sides.items():
                for nonIdx, non in enumerate(side.activeNons):
                    if non.name == nonName:
                        return (sideId, nonIdx)
                for nonIdx, non in enumerate(side.notActiveNons):
                    if non.name == nonName:
                        return (sideId, nonIdx)
            return False
        else:
            for nonIdx, non in enumerate(self.sides[sideId].activeNons):
                if non.name == nonName:
                    return (sideId, nonIdx)
            for nonIdx, non in enumerate(self.sides[sideId].notActiveNons):
                if non.name == nonName:
                    return (sideId, nonIdx)
            return False

    def updateWeather(self, weather: str, reason: str, org: tuple[str, int], **kwargs):
        # 尝试改变天气
        if self.weather == weather:
            self.log.append("天气没有任何变化……\n")
            return
        self.weather = weather
        self.log.append("由于[{}]天气变成了{}……\n".format(reason, self.weather))
        kwargs["weatherChangedOrg"] = org
        self.eventTriggerAll("onWeatherChanged", **kwargs)

    def tuple2Non(self, nonTuple: tuple[str, int], active: bool = True):
        """给定一个non的tuple，返回该non对象。active用于指定他是否active

        Args:
            nonTuple (tuple[str, int]): _description_
            active (bool, optional): _description_. Defaults to True.

        Returns:
            _type_: _description_
        """
        if active:
            return self.sides[nonTuple[0]].activeNons[nonTuple[1]]
        return self.sides[nonTuple[0]].notActiveNons[nonTuple[1]]

    def haveNonToSwitch(self, sideId: str):
        """给定一个sideId，判断他是否有能够换上来的备战NON

        Args:
            sideId (str): _description_

        Returns:
            _type_: _description_
        """
        for non in self.sides[sideId].notActiveNons:
            if non.hp > 0:
                # print(non.name)
                return True
        return False


def getNonEntity(masterId: str, nonName: str) -> NON | bool:
    """从json获取NON实体

    Args:
        masterId (str): _description_
        nonName (str): _description_

    Returns:
        NON | bool: _description_
    """
    makeSureDir(baseNonFilePath + "{}/NON/".format(masterId))
    path = baseNonFilePath + "{}/NON/{}.json".format(masterId, nonName)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            non = NON(**load(f))
        # non.toEntity()
        return non
    else:
        # Oh fuck! It's impossible!
        return False
