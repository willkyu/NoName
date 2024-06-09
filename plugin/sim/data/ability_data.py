from __future__ import annotations
from ..ability import Ability
from ..non_events import NonEvent, NonEventsObj
from .ability_function import AbilityFunctions


ability_data_base: list[Ability] = [
    Ability(
        id=1,
        name="Hello World",
        name_cn="你好世界",
        desc="“print('Hello World')”\n出场时所有队友攻击等级+1.",
        add_non_events=NonEventsObj(
            on_active_once=[
                NonEvent(reason="你好世界", exe=AbilityFunctions.hello_world)
            ]
        ),
    ),
    Ability(
        id=2,
        name="Absolute Fairness",
        name_cn="绝对公平",
        desc="出场时场上所有等级变化归零.",
        add_non_events=NonEventsObj(
            on_active_once=[
                NonEvent(reason="绝对公平", exe=AbilityFunctions.absolute_fairness)
            ]
        ),
    ),
    Ability(
        id=3,
        name="Reborn",
        name_cn="死者苏生",
        desc="出场时场上所有死亡的NON以一半的血量复活.",
        add_non_events=NonEventsObj(
            on_active_once=[NonEvent(reason="死者苏生", exe=AbilityFunctions.reborn)]
        ),
    ),
    Ability(
        id=4,
        name="Water Stepping",
        name_cn="踩踩水花",
        desc="变为雨天时速度上升.",
        add_non_events=NonEventsObj(
            on_weather_changed=[
                NonEvent(reason="踩踩水花", exe=AbilityFunctions.water_stepping)
            ]
        ),
    ),
    Ability(
        id=5,
        name="Reluctant",
        name_cn="不舍",
        desc="回到后备时给队友回复一定血量.",
        add_non_events=NonEventsObj(
            on_active_once=[NonEvent(reason="不舍", exe=AbilityFunctions.reluctant)]
        ),
    ),
    Ability(
        id=6,
        name="Knee Jerk",
        name_cn="膝跳反射",
        desc="收到物理攻击时对攻击方造成一定伤害.",
        add_non_events=NonEventsObj(
            on_hit=[NonEvent(reason="膝跳反射", exe=AbilityFunctions.knee_jerk)]
        ),
    ),
]


ability_data_dict_en: dict[str, Ability] = {
    ability_data.name: ability_data for ability_data in ability_data_base
}

ability_data_dict_cn: dict[str, Ability] = {
    ability_data.name_cn: ability_data for ability_data in ability_data_base
}
