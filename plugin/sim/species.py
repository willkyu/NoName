from dataclasses import dataclass
from .ability import SpeciesAbilities
from .global_utils import Type


@dataclass
class RateBuff:
    spring_rate_buff: int
    summer_rate_buff: int
    autumn_rate_buff: int
    winter_rate_buff: int

    # 时间段,int对应该时段最后时间点
    # class TimePeriod(Enum):
    #     MORNING = "早晨"
    #     NOON = "中午"
    #     AFTERNOON = "下午"
    #     NIGHT = "夜晚"
    morning_rate_buff: int
    noon_rate_buff: int
    afternoon_rate_buff: int
    night_rate_buff: int


@dataclass
class SpeciesStrength:
    HP: int = 0
    ATK: int = 0
    DEF: int = 0
    SPA: int = 0
    SPD: int = 0
    SPE: int = 0


@dataclass
class SpeciesData:
    name: str
    name_cn: str
    index: int
    types: list[Type]
    abilities: SpeciesAbilities
    species_strength: SpeciesStrength
    desc: str

    """
    出现率相关
    地域
    时间
    季节
    """
    # 我觉得liveArea在这里可以不写，直接在area那里调用找这里的概率就行
    # liveArea: list[str]
    move_learn_set: dict[int, str] = None  # {learnAtLevel: moveName}

    gender_rate: float | None = 0.5  # male rate

    base_rate_buff: int = 5

    rate_buff: RateBuff = None

    # TODO
    pass

    def __post_init__(self):
        if self.move_learn_set is None:
            self.move_learn_set = {
                1: "Tackle",
                2: "Tackle",
                3: "Tackle",
                4: "Tackle",
            }

    def __str__(self):
        species_str = ""
        species_str += f"{self.name_cn} {self.name}, No.{self.index}\nTypes: "
        species_str += ", ".join(self.types)
        species_str += (
            f"\nAbilities: {self.abilities.A1}, {self.abilities.A2} and ???\n"
        )
        species_str += f"HP: {self.species_strength.HP}, ATK: {self.species_strength.ATK}, DEF: {self.species_strength.DEF}, SPA: {self.species_strength.SPA}, SPD: {self.species_strength.SPD}, SPE: {self.species_strength.SPE}\n"
        species_str += self.desc
        return species_str


def getSpeciesRateBuff(species: SpeciesData):
    species.rate_buff.spring_rate_buff
    species.rate_buff.night_rate_buff
    # do what you want
    res = 0
    pass
    return res
