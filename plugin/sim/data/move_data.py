from functools import partial
from ..move import MoveData
from .move_function import MoveFunctions


move_data_base: list[MoveData] = [
    MoveData(
        id=1,
        name="Tackle",
        name_cn="撞击",
        pp=40,
        category="Physical",
        type="Normal",
        target="normal",
        base_power=40,
        accuracy=100,
        desc="使用全身的力气撞击目标。",
    ),
    MoveData(
        id=2,
        name="Ember",
        name_cn="火花",
        pp=30,
        category="Magical",
        type="Fire",
        target="normal",
        base_power=40,
        accuracy=100,
        desc="向目标发射小小的火苗。有时会令目标烧伤.",
        secondary=partial(MoveFunctions.may_burnt, chance=0.25),
    ),
]

move_data_dict_en: dict[str, MoveData] = {
    moveData.name: moveData for moveData in move_data_base
}

move_data_dict_cn: dict[str, MoveData] = {
    moveData.name_cn: moveData for moveData in move_data_base
}
