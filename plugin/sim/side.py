from typing import Any, Literal
from __future__ import annotations

from plugin.sim.state import State
from sim.nonClass import NONBattleEntity, EffectState
from sim.battle import Battle
from sim.globalTypes import *


class ChosenAction:
    """A single action that can be chosen."""

    choice: Literal[
        "move", "switch", "instaswitch", "revivalblessing", "team", "shift", "pass"
    ]  # action type
    non: NONBattleEntity | None  # the NONBattleEntity doing the action
    targetLoc: (
        number | None
    )  # relative location of the target to NONBattleEntity (move action only)
    moveid: str  # a move to use (move action only)
    move: (
        ActiveMove | None
    )  # the active move corresponding to moveid (move action only)
    target: NONBattleEntity | None  # the target of the action
    index: number | None  # the chosen index in Team Preview
    side: Side | None  # the action's side
    priority: number | None  # priority of the action


class Choice:
    """What the player has chosen to happen."""

    cantUndo: (
        bool  # true if the choice can't be cancelled because of the maybeTrapped issue
    )
    error: str  #  contains error text in the case of a choice error
    actions: list[ChosenAction]  # array of chosen actions
    forcedSwitchesLeft: number  #  number of switches left that need to be performed
    forcedPassesLeft: number  #  number of passes left that need to be performed
    switchIns: set[number]  #  indexes of NONBattleEntity chosen to switch in
    zMove: bool  #  true if a Z-move has already been selected
    mega: bool  #  true if a mega evolution has already been selected
    ultra: bool  #  true if an ultra burst has already been selected
    dynamax: bool  #  true if a dynamax has already been selected
    terastallize: bool  #  true if a terastallization has already been inputted

    def __init__(self, choiceDict: dict) -> None:
        self.__dict__.update(choiceDict)
        pass


class Side:
    battle: Battle
    id: SideID
    n: number  # Index in `battle.sides`: `battle.sides[side.n] === side`

    name: str
    avatar: str
    foe: Side = None
    allySide: Side | None = None  # Only exists in multi battle, for the allied side
    team: list[NonSet]
    non: list[NONBattleEntity]
    active: list[NONBattleEntity]

    faintedLastTurn: NONBattleEntity | None
    faintedThisTurn: NONBattleEntity | None
    totalFainted: number

    # these point to the same object as the ally's, in multi battles
    sideConditions: dict[list[SideID, str], EffectState]
    slotConditions: list[dict[list[SideID, str], EffectState]]

    activeRequest: object | None
    choice: Choice

    def __init__(
        self, name: str, battle: Battle, sideNum: number, team: list[NonSet]
    ) -> None:
        self.readonlyList = ["battle", "id", "n"]
        sideScripts = battle.dex.data.Scripts.side
        if sideScripts:
            self.__dict__.update(sideScripts)

        self.battle = battle
        self.id = ["p1", "p2", "p3", "p4"][sideNum]
        self.n = sideNum

        self.name = name
        self.avatar = ""

        self.team = team
        self.non = []
        for i in range(min(len(self.team), 24)):
            self.non.append(NONBattleEntity(self.team[i], self))
            self.non[i].position = i

        match self.battle.gameType:
            case "doubles":
                self.active = [None, None]
            case "triples" | "rotation":
                self.active = [None, None, None]
            case _:
                self.active = [None]

        self.nonLeft = len(self.non)
        self.faintedLastTurn - None
        self.faintedThisTurn = None
        self.totalFainted = 0

        self.sideConditions = {}
        self.slotConditions = []

        for i in range(len(self.active)):
            self.slotConditions[i] = {}

        self.activeRequest = None
        self.choice = Choice(
            {
                "cantUndo": False,
                "error": "",
                "actions": [],
                "forcedSwitchesLeft": 0,
                "forcedPassesLeft": 0,
                "switchIns": set(),
                "zMove": False,
                "mega": False,
                "ultra": False,
                "dynamax": False,
                "terastallize": False,
            }
        )

    def toJSON(self) -> any:
        return State.serializeSide(self)

    @property
    def requestState(self) -> RequestState:
        if not self.activeRequest or self.activeRequest.wait:
            return ""
        if self.activeRequest.teamPreview:
            return "teampreview"
        if self.activeRequest.forceSwitch:
            return "switch"
        return "move"

    def getChoice(self) -> Choice:
        if len(self.choice.actions) > 1 and all(
            action.choice == "team" for action in self.choice.actions
        ):
            return "team " + ", ".join(
                str(action.non.position + 1) for action in self.choice.actions
            )
        returnList = []
        for action in self.choice.actions:
            match action.choice:
                case "move":
                    if action.targetLoc and len(self.active):
                        returnList.append(
                            "move {}{}".format(
                                action.moveid,
                                " {}{}".format(
                                    "+" if action.targetLoc > 0 else "",
                                    action.targetLoc,
                                ),
                            )
                        )
                case "switch" | "instaswitch" | "revivalblessing":
                    returnList.append("switch {}".format(action.target.position + 1))
                case "team":
                    returnList.append("team {}".format(action.non.position + 1))
                case _:
                    returnList.append(action.choice)
        return ", ".join(returnList)

    # TODO
    pass

    def __setattr__(self, name: str, value: Any) -> None:
        if name in self.readonlyList:
            pass
        else:
            super(Side, self).__setattr__(name, value)
