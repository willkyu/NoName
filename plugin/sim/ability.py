from dataclasses import dataclass

from .non_events import NonEventsObj


@dataclass
class Ability:
    id: int
    name: str
    name_cn: str
    desc: str
    # 是否影响天气，这个应该放在flag里
    # suppressWeather: bool
    # 一些布尔型flag
    flags: dict[str, bool] = None

    add_non_events: NonEventsObj = None

    # TODO
    def __post_init__(self):
        if self.flags is None:
            self.flags = {}
        if self.add_non_events is None:
            self.add_non_events = NonEventsObj()

    def __str__(self) -> str:
        ability_str = ""
        ability_str += f"{self.name_cn} {self.name}\n{self.desc}"
        return ability_str


@dataclass
class SpeciesAbilities:
    A1: str  # ability 1
    A2: str  # ability 2
    H: str  # hidden ability
