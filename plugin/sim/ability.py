from sim.globalUtils import *
from sim.nonEvents import *


@dataclass
class Ability:
    name: str
    cnName: str
    desc: str
    # 是否影响天气，这个应该放在flag里
    # suppressWeather: bool
    # 一些布尔型flag
    flags: dict[str, bool]

    addNonEvents: NonEventsObj
    # TODO


@dataclass
class SpeciesAbilities:
    A1: Ability
    A2: Ability
    H: Ability
