from sim.globalUtils import *
from sim.ability import Ability


@dataclass
class SpeciesData:
    name: str
    idex: int
    types: list[str]
    abilities: dict[str, Ability]

    # TODO
    pass
