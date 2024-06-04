from sim.globalUtils import *
from sim.species import SpeciesData
from sim.ability import Ability
from sim.nonEvents import NonEventsObj


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


@dataclass
class NON(object):
    name: str
    masterId: str
    species: SpeciesData
    level: LevelRange
    gender: Literal["M", "F", "N"]
    inBattle: str  # should be '' if not in battle
    item: str
    battleStatus: NonTempBattleStatus
    ability: Ability
    nonEvents: NonEventsObj

    moveSlots: list[MoveSlot]
    ivs: IVs
    evs: EVs

    statDict: dict[str, int] = {k: 0 for k in statList}

    def save(self):
        self.dump2Json()

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
