from sim.globalUtils import *


@dataclass
class Ability:
    # 是否影响天气
    suppressWeather: bool
    # 一些布尔型flag
    flags: dict[str, bool]
    # TODO
