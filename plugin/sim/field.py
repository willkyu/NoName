from sim.globalUtils import *
from sim.non import NON
from sim.command import Command
from sim.player import Player


class Side:
    nonNum: Literal[1, 2]
    activeNons: list[NON]
    notActiveNons: list[NON]

    commandList: dict[int, Command]

    # 一些其他的东西，如护盾
    shield: bool = False

    def __init__(self, team: list[NON], battleMode: BattleMode) -> None:
        self.nonNum = 2 if battleMode == "double" else 1
        self.activeNons, self.notActiveNons = team[: self.nonNum], team[self.nonNum :]
        self.commandList = {}

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

        self.commandList[index] = Command
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
            moveslot.move for moveslot in self.activeNon[index].moveSlots
        ]:
            return "无法使用该NON不会的招式"
        # 这之后可以再加别的检查合法性，比如不能交换状态进行交换
        return True

    def calculateCommandSpeed(self, commandIndex: int) -> int:
        # 计算指令的NON的当前速度
        pass

    pass


class Field:
    sides: dict[str, Side]  # {userId: Side}
    nonTeamDict: dict[str, list[NON]]  # {userId:[NON]}

    weather: str = "Normal"

    # 一些其他的东西
    lastUsedMove: str | None = None

    pass

    def __init__(
        self,
        playerList: Annotated[list[Player], "len should be 2 or 4"],
        battleMode: BattleMode,
    ) -> None:
        self.nonTeamDict = {
            player.id: [Field.getNonEntity(non) for non in player.team]
            for player in playerList
        }
        self.sides = {
            player.id: Side(self.nonTeamDict[player.id], battleMode)
            for player in playerList
        }

        # 下面这里不太对，应该在battle里写
        # for player in playerList:
        #     for non in self.nonTeamDict:
        #         non.inBattle=True

        pass

    def exeCommand(self, sideId: str, commandIndex: int):
        # do this command
        command: Command = self.sides[sideId].commandList[commandIndex]
        pass

    def calculateCommandOrder(self):
        # 计算指令的顺序，同优先级下速度快的优先
        commandDict: dict[tuple[str, int], Command] = {}
        for sideId, side in self.sides.items():
            for commandIndex, command in side.commandList.items():
                commandDict[(sideId, commandIndex):command]

        # calculate the order
        self.updateCommandPriority()
        commandPriorityDict = {
            commandTuple: (
                command.priority,
                self.sides[commandTuple[0]].calculateCommandSpeed(commandTuple[1]),
            )
            for commandTuple, command in commandDict.items()
        }

        return [
            key
            for key, value in sorted(
                commandPriorityDict.items(), key=lambda x: (-x[1][0], -x[1][1])
            )
        ]

    def updateCommandPriority(
        self, commandDict: dict[tuple[str, int], Command]
    ) -> None:
        # 特殊情况下的优先级更新，比如追击
        pass

    @staticmethod
    def getNonEntity(masterId: str, nonName: str) -> NON | bool:
        # 从json获取NON实体
        path = baseNonFilePath + "{}/NON/{}.json".format(masterId, nonName)
        if os.path.exists(path):
            with open(path, "r") as f:
                non = NON(load(f))
            return non
        else:
            # Oh fuck! It's impossible!
            return False
