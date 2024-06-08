from dataclasses import dataclass

from .non_events import NonEventsObj


@dataclass
class Ability:
    name: str
    name_cn: str
    desc: str
    # 是否影响天气，这个应该放在flag里
    # suppressWeather: bool
    # 一些布尔型flag
    flags: dict[str, bool]

    add_non_events: NonEventsObj
    # TODO

    def __str__(self) -> str:
        return self.name_cn


@dataclass
class SpeciesAbilities:
    A1: str  # ability 1
    A2: str  # ability 2
    H: str  # hidden ability
