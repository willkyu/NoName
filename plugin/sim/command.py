from .globalUtils import *

# from sim.data.moveData import moveDataDictEn


@dataclass
class Command:
    target: str | None
    action: Literal["switch", "retire", "specialEvo", "move", "item"]
    move: str | None
    priority: int = 0
    targetTuple: tuple[str, int] = None

    def __post_init__(self):
        if self.action == "move":
            self.priority = getMovePriority(self.move)
        else:
            self.priority = 10


def getMovePriority(move: str) -> int:
    return moveDataDictEn[move].priority
    pass
