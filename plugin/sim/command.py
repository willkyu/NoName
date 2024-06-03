from sim.globalUtils import *


@dataclass
class Command:
    target: str | None
    action: Literal["switch", "retire", "specialEvo", "move", "item"]
    move: str | None
    priority: int = 0

    def __post_init__(self):
        if self.action == "move":
            self.priority = getMovePriority(self.move)
        else:
            self.priority = 10


def getMovePriority(move: str) -> int:
    pass
