from __future__ import annotations
from ..ability import Ability
from ..non_events import NonEvent, NonEventsObj
from .ability_function import AbilityFunctions


ability_data_base: list[Ability] = [
    Ability(
        id=1,
        name="Hello World",
        name_cn="你好世界",
        desc="出场时所有队友攻击等级+1.",
        add_non_events=NonEventsObj(
            on_active_once=[
                NonEvent(reason="你好世界", exe=AbilityFunctions.hello_world)
            ]
        ),
    ),
    Ability(id=2, name="", name_cn="", desc="", add_non_events=NonEventsObj()),
]

# Ability(id=2, name="", name_cn="", desc="", add_non_events=NonEventsObj()),


ability_data_dict_en: dict[str, Ability] = {
    ability_data.name: ability_data for ability_data in ability_data_base
}

ability_data_dict_cn: dict[str, Ability] = {
    ability_data.name_cn: ability_data for ability_data in ability_data_base
}
