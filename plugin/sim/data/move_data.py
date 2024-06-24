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
        pp=35,
        category="Magical",
        type="Fire",
        target="normal",
        base_power=40,
        accuracy=100,
        desc="向目标发射小小的火苗。有时会令目标烧伤.",
        secondary=partial(MoveFunctions.may_burnt, chance=0.25),
    ),
    MoveData(
        id=3,
        name="Fallout",
        name_cn="原子尘埃",
        pp=5,
        category="Auxiliary",
        type="Normal",
        target="normal",
        # base_power=40,
        accuracy=80,
        desc="“远离它.”\n令目标陷入污染状态.",
        condition=partial(MoveFunctions.may_pollution, chance=1),
    ),
    MoveData(
        id=4,
        name="Radiation",
        name_cn="核辐射",
        pp=1,
        category="Auxiliary",
        type="Normal",
        target="all",
        # base_power=40,
        accuracy=100,
        desc="“STOP.”\n令场上所有NON陷入污染状态.",
        condition=partial(MoveFunctions.may_pollution_all, chance=1),
    ),
    MoveData(
        id=5,
        name="One Punch",
        name_cn="一拳",
        pp=20,
        category="Magical",
        type="Normal",
        target="normal",
        base_power=60,
        accuracy=True,
        desc="这是魔法的一拳.",
    ),
    MoveData(
        id=6,
        name="Strike",
        name_cn="闪击",
        pp=10,
        category="Physical",
        type="Normal",
        target="normal",
        base_power=30,
        accuracy=100,
        priority=1,
        desc="以迅雷不及掩耳盗铃之势的进攻，真的好快.",
    ),
    MoveData(
        id=7,
        name="Protect",
        name_cn="保护",
        pp=10,
        category="Auxiliary",
        type="Normal",
        target="normal",
        # base_power=60,
        accuracy=True,
        desc="打架是不好的.",
        condition=MoveFunctions.protect,
    ),
    MoveData(
        id=8,
        name="Pray for rain",
        name_cn="祈雨",
        pp=10,
        category="Auxiliary",
        type="Water",
        target="all",
        # base_power=60,
        accuracy=True,
        desc="龙王现身.",
        condition=MoveFunctions.pray_for_rain,
    ),
]

move_data_dict_en: dict[str, MoveData] = {
    moveData.name: moveData for moveData in move_data_base
}

move_data_dict_cn: dict[str, MoveData] = {
    moveData.name_cn: moveData for moveData in move_data_base
}
