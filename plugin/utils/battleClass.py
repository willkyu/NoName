from utils.nonClass import NONBattleEntity


class PlayerCommand(object):
    def __init__(self, userID: str, num: int) -> None:
        self.id = userID
        self.commandDict = {}
        self.commandArgs = {}
        pass


class BattleStage(object):
    def __init__(self) -> None:
        self.stage = ""
        self.weather = ""
        self.NonDict = {}
        self.playerNonBattle = {}
        self.playerNonBattleNum = 0
        self.playerNonParty = {}
        pass

    def addPlayer(self, nonList: list[NONBattleEntity], playerID: str):
        self.playerNonBattle[playerID] = nonList[: self.playerNonBattleNum]
        self.playerNonParty[playerID] = nonList[self.playerNonBattleNum :]


class Battle(object):
    def __init__(self, groupID: str, botSendFunc: function) -> None:
        self.playerDict: dict[str, PlayerCommand]
        self.nonNum: int
        self.logger: str
        self.sequence: list[tuple[str, int]]  # (PlayerID, index)

        self.groupID = groupID
        self.botSend = botSendFunc
        self.playerDict = {}
        self.nonNum = 0
        self.logger = ""
        self.start = False
        self.sequence = []
        self.battleStage = BattleStage()
        pass

    def processOneTurn(self):
        for playerID, index in self.sequence:
            # if can use move
            pass

            self.playerDict[playerID].commandDict[index].exe(
                self.battleStage,
                self.botSend,
                **self.playerDict[playerID].commandArgs[index]
            )

    def log(self, loginfo: str):
        self.logger += loginfo

    def addPlayer(self, playerID):
        self.playerDict[playerID] = PlayerCommand(playerID, num=1)
