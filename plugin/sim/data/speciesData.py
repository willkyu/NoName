from sim.species import *
from sim.data.abilityData import abilityDataDictEn

normalRateBuff = RateBuff([5] * 8)

speciesDataBase = list[SpeciesData] = [
    SpeciesData(
        name="NillKyu",
        idex=1,
        types="Normal",
        abilities=SpeciesAbilities(
            A1=abilityDataDictEn["Hello World"],
            A2=abilityDataDictEn["Hello World"],
            H=abilityDataDictEn["Hello World"],
        ),
        liveArea=["平原", "沼泽"],
        rateBuff=normalRateBuff,
    )
]
