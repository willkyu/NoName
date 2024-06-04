from sim.species import *
from sim.data

normalRateBuff = RateBuff([5] * 8)

speciesDataBase = list[SpeciesData] = [
    SpeciesData(
        name="NillKyu", idex=1, types='Normal',abilities=SpeciesAbilities(A1=),liveArea=["平原", "沼泽"], rateBuff=normalRateBuff
    )
]
