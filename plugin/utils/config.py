import os
from plugin.utils.sim.battleClass import Battle


def dir(path: str) -> str:
    if not os.path.exists(path):
        os.mkdir(path)
    return path


class Config(object):
    def __init__(self, groupList: list[str], masterList: list[str]) -> None:
        self.battleList: list[Battle]

        self.groupList = groupList
        self.masterList = masterList
        self.bagPath = dir("./plugin/data/ChanceCustom/Mance/数据/背包/")
        self.NoNPath = dir("./plugin/data/NoName/")
        self.battlePlayerDict = {}
        self.battleGroupDict = {}
        self.battleList = []
        pass

    def updateList(self, ID: str, addMode: bool = True, groupMode: bool = True) -> None:
        if addMode:
            if groupMode and ID not in self.groupList:
                self.groupList.append(ID)
            elif not groupMode and ID not in self.masterList:
                self.masterList.append(ID)
        else:
            if groupMode and ID in self.groupList:
                self.groupList.remove(ID)
            elif not groupMode and ID in self.masterList:
                self.masterList.remove(ID)

    def updateBattleStatus(self, battlePlayerDict, battleGroupDict):
        self.battlePlayerDict = battlePlayerDict
        self.battleGroupDict = battleGroupDict
