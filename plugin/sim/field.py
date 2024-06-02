from sim.globalUtils import *
from sim.non import NON
from sim.command import Command


class Side:
    activeNon: list[NON]
    notActiveNon: list[NON]

    commandList: list[Command]

    # 一些其他的东西，如护盾
    shield: bool = False

    pass


class Field:
    sides: dict[str, Side]  # {userId: Side}
    weather: str = "Normal"

    # 一些其他的东西
    lastUsedMove: str | None = None

    pass
