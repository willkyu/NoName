from .globalUtils import *
from .nonEvents import *

# from sim.data.abilityData import abilityDataDictEn


@dataclass
class Condition:
    name: str
    cnName: str
    desc: str
    # 是否影响天气，这个应该放在flag里
    # suppressWeather: bool
    # 一些布尔型flag
    flags: dict[str, bool]

    addNonEvents: NonEventsObj
    # TODO

    def __str__(self) -> str:
        return self.cnName
