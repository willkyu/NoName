from random import shuffle
import math

from sim.globalUtils import *
from sim.non import NON, MoveSlot
from sim.command import Command
from sim.player import Player
from sim.nonEvents import NonEventsObj


class Side:
    nonNum: Literal[1, 2]
    activeNons: list[NON]
    notActiveNons: list[NON]

    commandDict: dict[int, Command]

    # 一些其他的东西，如护盾
    shield: bool = False

    def __init__(self, team: list[NON], battleMode: BattleMode) -> None:
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
        print("{}已添加:\n{}\n".format(index, command))
        return True

    def checkCommandValid(self, index: int, command: Command) -> str | bool:
        """检查指令合法性，如果合法返回True，否则是str，描述不合法原因

        Args:
            index (int): 指令的位置（哪个NON进行操作）
            command (Command): _description_

        Returns:
            str|bool: _description_
        """
        if command.move not in [
            moveslot for moveslot in self.activeNons[index].moveSlots.keys()
        ]:
            return "无法使用该NON不会的招式"
        # 这之后可以再加别的检查合法性，比如不能交换状态进行交换
        return True

    def calculateNonSpeed(self, commandIndex: int) -> int:
        # 计算指令的NON的当前速度
        non = self.activeNons[commandIndex]
        return non.stat.SPE
        pass

    def getAllCommand(self) -> bool:
        if None in self.commandDict.values():
            return False
        return True

    pass


class Field:
    sides: dict[str, Side]  # {userId: Side}
    nonTeamDict: dict[str, list[NON]]  # {userId:[NON]}
    log: list[str]
    waitSwitchDict: dict[str, list[int]] = None

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
        self.nonTeamDict = {
            player.id: [getNonEntity(player.id, non) for non in player.team]
            for player in playerList
        }
        self.sides = {
            player.id: Side(self.nonTeamDict[player.id], battleMode)
            for player in playerList
        }
        self.log = log

        self.waitSwitchDict = {}

        # 下面这里不太对，应该在battle里写
        # for player in playerList:
        #     for non in self.nonTeamDict:
        #         non.inBattle=True

        pass

    def exeCommand(self, sideId: str, commandIndex: int):
        # * 注意，exeCommand之前必须确保指令可行，也就是在addCommand阶段就要检查指令可行性
        # do this command
        command: Command = self.sides[sideId].commandDict[commandIndex]
        match command.action:
            case "retire":
                # sideId输
                pass
            case "switch":
                targetNonIndex = self.getNonTuple(command.target)[1]
                self.eventTriggerSingle("beforeSwitch", (sideId, commandIndex))
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

        pass

    def exeMove(self, sideId: str, commandIndex: int):
        command: Command = self.sides[sideId].commandDict[commandIndex]
        non = self.tuple2Non((sideId, commandIndex))
        non.moveSlots[command.move].pp -= 1
        targetTuple = self.getNonTuple(command.target)
        targetNon = self.tuple2Non(targetTuple)
        if non.moveSlots[command.move].move.category != "Auxiliary":
            damage = self.calculateDamage(
                non,
                non.moveSlots[command.move],
                targetNon,
            )
            self.log.append(
                "{}受到了{}点伤害，还剩{}HP.".format(
                    command.target, damage, targetNon.hp - damage
                )
            )
            targetNon.hp -= damage
            if targetNon.hp <= 0:
                self.faintedProcess(targetTuple)
        else:
            # 辅助招式
            pass

        pass

    def faintedProcess(self, targetTuple: tuple[str, int]):
        self.log.append(
            "[{}]的[{}]倒下了……".format(
                getNickname(targetTuple[0]), self.tuple2Non(targetTuple).name
            )
        )
        if self.haveNonToSwitch(targetTuple[0]):
            self.waitSwitchDict[targetTuple]
        self.waitSwitchDict[targetTuple[0]].append(targetTuple[1])
        pass

    def calculateDamage(self, orgNon: NON, move: MoveSlot, targetNon: NON):
        multiply = 1.0
        category = move.move.category
        # TODO 计算属性克制倍率
        damage = multiply * (
            (2 * orgNon.level + 10)
            / 250
            * (orgNon.stat.ATK if category == "Physical" else orgNon.stat.SPA)
            / (targetNon.stat.DEF if category == "Physical" else targetNon.stat.SPD)
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
                commandDict[(sideId, commandIndex)] = command

        # calculate the order
        self.updateCommandPriority(commandDict)
        commandPriorityDict = {
            commandTuple: (
                command.priority,
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
        nonSpeedDict: dict[tuple[str, int], NON] = {}

        # 使用shuffle打乱顺序，实现相同速度下的随机排序
        shuffledSideList = self.sides.items()
        shuffle(shuffledSideList)

        for sideId, side in shuffledSideList:
            for nonIdx in len(side.activeNons):
                nonSpeedDict[(sideId, nonIdx)] = side.calculateNonSpeed(nonIdx)

        returnList = [
            key for key in sorted(nonSpeedDict.keys(), key=lambda x: (-nonSpeedDict[x]))
        ]
        if returnNonEntity:
            newreturnList = [self.tuple2Non(nonTuple) for nonTuple in returnList]
            return returnList, newreturnList
        return returnList

    def updateCommandPriority(
        self, commandDict: dict[tuple[str, int], Command]
    ) -> None:
        # 特殊情况下的优先级更新，比如追击
        pass

    def eventTriggerAll(self, eventName: str, **kwargs):
        if not hasattr(NonEventsObj, eventName):
            return
        for non, nonTuple in self.calculateSpeedOrder(returnNonEntity=True):
            kwargs.update({"org": nonTuple})
            eval("non.nonEvents.{}.exe(self,**kwargs)".format(eventName))

    def eventTriggerSingle(self, eventName: str, nonTuple: tuple[str, int], **kwargs):
        if not hasattr(NonEventsObj, eventName):
            return
        non = self.tuple2Non(nonTuple)
        kwargs.update({"org": nonTuple})
        eval("non.nonEvents.{}.exe(self,**kwargs)".format(eventName))

    def getNonTuple(self, nonName: str, sideId: str = None):
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
        if self.weather == weather:
            self.log.append("天气没有任何变化……\n")
            return
        self.weather = weather
        self.log.append("由于[{}]天气变成了{}……\n".format(reason, self.weather))
        kwargs["weatherChangedOrg"] = org
        self.eventTriggerAll("onWeatherChanged", **kwargs)

    def tuple2Non(self, nonTuple: tuple[str, int], active: bool = True):
        if active:
            return self.sides[nonTuple[0]].activeNons[nonTuple[1]]
        return self.sides[nonTuple[0]].notActiveNons[nonTuple[1]]

    def haveNonToSwitch(self, sideId: str):
        for non in self.sides[sideId].notActiveNons:
            if non.hp > 0:
                return True
        return False


def getNonEntity(masterId: str, nonName: str) -> NON | bool:
    # 从json获取NON实体
    path = baseNonFilePath + "{}/NON/{}.json".format(masterId, nonName)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            non = NON(**load(f))
        # non.toEntity()
        return non
    else:
        # Oh fuck! It's impossible!
        return False
