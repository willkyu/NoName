import math

from sim.globalUtils import *
from sim.species import SpeciesData
from sim.ability import Ability
from sim.data.abilityData import abilityDataDictEn
from sim.nonEvents import NonEventsObj
from sim.data.speciesData import speciesDataDictEn


@dataclass
class MoveSlot:
    name: str
    id: str = None
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
        self.toEntity()  # only test
        if self.stat == None:
            self.calculateStat()

    def calculateStat(self):
        HP: int
        statDict = {}
        for stat in statList:
            self.species.speciesStrength.HP
            self.ivs.HP
            self.evs.HP
            statDict[stat] = eval(
                "math.floor({}+(self.level*(2*self.species.speciesStrength.{}+self.ivs.{}+math.sqrt(self.evs.{}) / 8))/100)".format(
                    10 if stat == "HP" else 5, stat, stat, stat
                )
            )
        self.hpmax = statDict["HP"]
        self.hp = statDict["HP"]
        self.stat = StatValue(**{k: v for k, v in statDict.items() if k != "HP"})

    def save(self):
        self.dump2Json()

    def dump2Json(self, test=False):
        if not test:
            self.toStr()
        path = baseNonFilePath + "{}/NON/".format(self.masterId)
        if test:
            path = "./"
        makeSureDir(path)
        # print(os.path.abspath(path))
        with open(path + "{}.json".format(self.name), "w+", encoding="utf-8") as f:
            dump(self, f, default=lambda obj: obj.__dict__, ensure_ascii=False)
        self.toEntity()

    def toEntity(self):
        self.ivs = IVs(**self.ivs)
        self.evs = EVs(**self.evs)
        if self.stat is not None:
            self.stat = StatValue(**self.stat)
        for k in self.moveSlots.keys():
            self.moveSlots[k] = MoveSlot(k)
        self.species = speciesDataDictEn[self.species]
        self.ability = abilityDataDictEn[self.ability]

    def toStr(self):
        self.ivs = self.ivs.__dict__
        self.evs = self.evs.__dict__
        for k in self.moveSlots.keys():
            self.moveSlots[k] = {"name": k}
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


def initNonFromSpecies(speciesName: str) -> NON:
    # TODO
    NON(
        name="测试NON",
        masterId="496373158",
        species="NillKyu",
        level=5,
        gender="N",
        inBattle="",
        ability="Hello World",
        moveSlots={"Tackle": {"name": "Tackle"}},
        ivs=IVs().__dict__,
        evs=EVs().__dict__,
    )
