from __future__ import annotations
from ..species import SpeciesData, RateBuff, SpeciesAbilities, SpeciesStrength
from .ability_data import ability_data_dict_cn

normal_rate_buff = RateBuff(*[5 for i in range(8)])

species_data_base: list[SpeciesData] = [
    SpeciesData(
        name="NillKyu",
        name_cn="拟Q",
        index=0,
        base_rate_buff=0,
        types=["Normal"],
        abilities=SpeciesAbilities(
            A1=ability_data_dict_cn["你好世界"],
            A2=ability_data_dict_cn["你好世界"],
            H=ability_data_dict_cn["你好世界"],
        ),
        rate_buff=normal_rate_buff,
        species_strength=SpeciesStrength(
            HP=100, ATK=100, DEF=100, SPA=100, SPD=100, SPE=100
        ),
        move_learn_set={1: "撞击"},
        desc="你不应该得到它.",
    ),
    SpeciesData(
        name="Sweericepling",
        name_cn="甜粽子",
        index=1,
        base_rate_buff=5,
        types=["Normal", "Water"],
        abilities=SpeciesAbilities(
            A1=ability_data_dict_cn["你好世界"],
            A2=ability_data_dict_cn["踩踩水花"],
            H=ability_data_dict_cn["死者苏生"],
        ),
        rate_buff=normal_rate_buff,
        species_strength=SpeciesStrength(HP=65, ATK=30, DEF=40, SPA=50, SPD=40, SPE=60),
        move_learn_set={
            1: "撞击",
            6: "保护",
            14: "祈雨",
            20: "闪击",
            26: "一拳",
            32: "原子尘埃",
        },
        desc="端午节快乐~大家该吃甜粽子啦.",
    ),
    SpeciesData(
        name="Saltricepling",
        name_cn="咸粽子",
        index=2,
        base_rate_buff=5,
        types=["Normal", "Fire"],
        abilities=SpeciesAbilities(
            A1=ability_data_dict_cn["绝对公平"],
            A2=ability_data_dict_cn["不舍"],
            H=ability_data_dict_cn["膝跳反射"],
        ),
        rate_buff=normal_rate_buff,
        species_strength=SpeciesStrength(HP=65, ATK=50, DEF=40, SPA=30, SPD=40, SPE=60),
        move_learn_set={
            1: "撞击",
            6: "一拳",
            14: "火花",
            20: "闪击",
            26: "祈雨",
            32: "原子尘埃",
        },
        desc="端午节快乐~大家该吃咸粽子啦.",
    ),
]


species_data_dict_en: dict[str, SpeciesData] = {
    species_data.name: species_data for species_data in species_data_base
}

species_data_dict_cn: dict[str, SpeciesData] = {
    species_data.name_cn: species_data for species_data in species_data_base
}
