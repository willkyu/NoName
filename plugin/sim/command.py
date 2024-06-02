from sim.globalUtils import *


@dataclass
class Command:
    target: str | None
    move: str | None
