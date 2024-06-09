from dataclasses import dataclass

from .non_events import NonEventsObj


@dataclass
class Condition:
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
        condition_str = ""
        condition_str += f"{self.name_cn} {self.name}\n"
        condition_str += self.desc
        return condition_str
