from typing import Literal

from sim.globalTypes import *
from sim.battle import Battle


class BattleQueue:
    battle: Battle
    actionList: list[Action]

    def __init__(self, battle: Battle) -> None:
        self.battle = battle
        self.actionList = []
        queueScrips = battle.format_.queue or battle.dex.data.Scrips.queue
        if queueScrips:
            self.__dict__.update(queueScrips.__dict__)

    def shift(self):
        if len(self.actionList) > 0:
            return self.actionList.pop(0)
        return None

    def peek(self, end: bool | None) -> Action | None:
        return self.actionList[-1 if end else 0]

    def push(self, action: Action):
        self.actionList.append(action)
        return len(self.actionList)

    def unshift(self, action: Action):
        self.actionList = [action] + self.actionList
        return len(self.actionList)

    def entries(self):
        return enumerate(self.actionList)

    # TODO
    pass
