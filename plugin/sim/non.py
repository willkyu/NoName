from sim.globalUtils import *
from sim.species import SpeciesData
from sim.ability import Ability
from sim.data.abilityData import abilityDataDictEn
from sim.nonEvents import NonEventsObj
from sim.data.speciesData import speciesDataDictEn


@dataclass
class MoveSlot:
    id: str
    name: str
    nameCn: str = None
    move: MoveData = None
    pp: int = None
    maxpp: int = None
    used: bool = False
    target: str | None = None
    disabled: bool | str = False
    disabledSource: str | None = None

    def __post_init__(self):
        if self.name is not None:
            self.move = getMoveEn(self.name)
            self.id = self.move.id
            self.nameCn = self.move.nameCn
            self.pp = self.move.pp
            self.maxpp = self.pp


@dataclass
class NonTempBattleStatus:
    lastItem: str = ""
    usedItemThisTurn: bool = False


@dataclass
class NON(object):
    name: str
    masterId: str
    species: SpeciesData | str
    level: LevelRange
    gender: Literal["M", "F", "N"]
    inBattle: str  # should be '' if not in battle
    ability: Ability | str

    moveSlots: dict[str, MoveSlot]  # {moveNameEn, MoveSlot}
    ivs: IVs
    evs: EVs

    stat: StatValue = None
    hp: int = 0
    hpmax: int = 0
    battleStatus: NonTempBattleStatus | None = None
    nonEvents: NonEventsObj = None
    item: str = None
    statsLevel: StatLevel = None

    def __post_init__(self):
        self.statsLevel = StatLevel()
        self.nonEvents = NonEventsObj()
        self.battleStatus = NonTempBattleStatus()

    def save(self):
        self.dump2Json()

    def dump2Json(self, test=False):
        self.toStr()
        path = baseNonFilePath + "{}/NON/".format(self.masterId)
        if test:
            path = "./"
        makeSureDir(path)
        print(os.path.abspath(path))
        with open(path + "{}.json".format(self.name), "w+", encoding="utf-8") as f:
            dump(self, f, default=lambda obj: obj.__dict__, ensure_ascii=False)
        self.toEntity()

    def toEntity(self):
        self.species = speciesDataDictEn[self.species]
        self.ability = abilityDataDictEn[self.ability]

    def toStr(self):
        self.species = self.species.name
        self.ability = self.ability.name

    def loadFromJson(self, masterId: str, nonName: str):
        # 可能用不上，直接在外部定义一个从json读类的就可以
        path = baseNonFilePath + "{}/NON/{}.json".format(masterId, nonName)
        if os.path.exists(path):
            with open(path, "r") as f:
                self.__dict__.update(load(f))
            return True
        else:
            return False
