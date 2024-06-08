from __future__ import annotations
from ..species import SpeciesData, RateBuff, SpeciesAbilities, SpeciesStrength
from .ability_data import ability_data_dict_en

normal_rate_buff = RateBuff(*[5 for i in range(8)])

species_data_base: list[SpeciesData] = [
    SpeciesData(
        name="NillKyu",
        name_cn="拟Q",
        idex=1,
        types="Normal",
        abilities=SpeciesAbilities(
            A1=ability_data_dict_en["Hello World"],
            A2=ability_data_dict_en["Hello World"],
            H=ability_data_dict_en["Hello World"],
        ),
        rate_buff=normal_rate_buff,
        species_strength=SpeciesStrength(
            HP=100, ATK=100, DEF=100, SPA=100, SPD=100, SPE=100
        ),
    )
]


species_data_dict_en: dict[str, SpeciesData] = {
    species_data.name: species_data for species_data in species_data_base
}

species_data_dict_cn: dict[str, SpeciesData] = {
    species_data.name_cn: species_data for species_data in species_data_base
}