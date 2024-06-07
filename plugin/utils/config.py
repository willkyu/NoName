import json
import os
from typing import Literal

baseDataFilePath = "./plugin/data/NoName/"


class Config:
    activeGroupList: list[str]
    masterList: list[str]

    def __init__(self) -> None:
        # global baseDataFilePath
        if not os.path.exists(baseDataFilePath + "config.json"):
            self.initConfigFile()
        with open(baseDataFilePath + "config.json", "r", encoding="utf-8") as f:
            self.__dict__.update(json.load(f))
            print(self.__dict__)

    def initConfigFile(self):
        self.activeGroupList = ["957736515"]
        self.masterList = ["496373158"]
        self.writeConfig()

    def writeConfig(self):
        with open(baseDataFilePath + "config.json", "w+", encoding="utf-8") as f:
            json.dump(self, f, default=lambda obj: obj.__dict__, ensure_ascii=False)

    def editConfig(
        self, ID: str, mode: Literal["group", "master"], addMode: bool = True
    ):
        if addMode:
            if mode == "group" and ID not in self.activeGroupList:
                self.activeGroupList.append(ID)
            elif mode == "master" and ID not in self.masterList:
                self.masterList.append(ID)
            else:
                return
        else:
            if mode == "group" and ID in self.activeGroupList:
                self.activeGroupList.remove[ID]
            elif mode == "master" and ID in self.masterList:
                self.masterList.remove[ID]
            else:
                return
        self.writeConfig()
