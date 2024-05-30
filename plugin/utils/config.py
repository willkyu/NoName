class Config(object):
    def __init__(self, groupList: list[str], masterList: list[str]) -> None:
        self.groupList = groupList
        self.masterList = masterList
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
