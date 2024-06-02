from sim.globalUtils import *
from sim.species import SpeciesData
from sim.ability import Ability


LevelRange = Annotated[int, Range(1, 100)]
IvRange = Annotated[int, Range(0, 31)]
EvRange = Annotated[int, Range(0, 252)]

statList = ["HP", "ATK", "DEF", "SPA", "SPD", "SPE"]


@dataclass
class IVs:
    HP: IvRange
    ATK: IvRange
    DEF: IvRange
    SPA: IvRange
    SPD: IvRange
    SPE: IvRange


@dataclass
class EVs:
    HP: EvRange
    ATK: EvRange
    DEF: EvRange
    SPA: EvRange
    SPD: EvRange
    SPE: EvRange

    def changeEv(self, ev: str, num: int, addMode: bool = True):
        if ev.upper() not in statList:
            print("Ev not valid!")
            return
        eval("self.{}{}={}".format(ev.upper(), "+" if addMode else "-", num))


@dataclass
class MoveSlot:
    id: str
    move: str
    pp: int
    maxpp: int
    used: bool
    target: str | None = None
    disabled: bool | str = False
    disabledSource: str | None = None


@dataclass
class NonTempBattleStatus:
    lastItem: str
    usedItemThisTurn: bool


class NON(object):
    name: str
    masterId: str
    species: SpeciesData
    level: LevelRange
    gender: Literal["M", "F", "N"]
    inBattle: str
    item: str
    battleStatus: NonTempBattleStatus
    ability: Ability

    moveSlots: list[MoveSlot]
    ivs: IVs
    evs: EVs

    statDict: dict[str, int] = {k: 0 for k in statList}

    def __init__(self) -> None:
        pass

    def dump2Json(self):
        path = baseNonFilePath + "{}/NON/".format(self.masterId)
        makeSureDir(path)
        with open(path + "{}.json".format(self.name), "w+") as f:
            dump(self, f)

    def loadFromJson(self, masterId: str, nonName: str):
        # 可能用不上，直接在外部定义一个从json读类的就可以
        path = baseNonFilePath + "{}/NON/{}.json".format(masterId, nonName)
        if os.path.exists(path):
            with open(path, "r") as f:
                self.__dict__.update(load(f))
            return True
        else:
            return False
