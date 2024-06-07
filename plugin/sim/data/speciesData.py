from ..species import *
from .abilityData import abilityDataDictEn

normalRateBuff = RateBuff(*[5 for i in range(8)])

speciesDataBase: list[SpeciesData] = [
    SpeciesData(
        name="NillKyu",
        nameCn="拟Q",
        idex=1,
        types="Normal",
        abilities=SpeciesAbilities(
            A1=abilityDataDictEn["Hello World"],
            A2=abilityDataDictEn["Hello World"],
            H=abilityDataDictEn["Hello World"],
        ),
        rateBuff=normalRateBuff,
        speciesStrength=SpeciesStrength(
            HP=100, ATK=100, DEF=100, SPA=100, SPD=100, SPE=100
        ),
    )
]


speciesDataDictEn: dict[str, SpeciesData] = {
    speciesData.name: speciesData for speciesData in speciesDataBase
}

speciesDataDictCn: dict[str, SpeciesData] = {
    speciesData.nameCn: speciesData for speciesData in speciesDataBase
}
