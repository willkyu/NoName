from ..non_events import NonEvent, NonEventsObj
from ..condition import Condition
from .condition_function import ConditionFunctions

# baseCondition = []

condition_data_base: list[Condition] = [
    Condition(
        name="Burnt",
        name_cn="烧伤",
        desc="烧伤不过百日长，你我都撑不起的未来，就让我来告别.",
        flags={"turn": 0},
        add_non_events=NonEventsObj(
            end_of_turn=[
                NonEvent(reason="烧伤", exe=ConditionFunctions.burnt_end_of_turn)
            ]
        ),
    )
]


condition_data_dict_en: dict[str, Condition] = {
    condition_data.name: condition_data for condition_data in condition_data_base
}

condition_data_dict_cn: dict[str, Condition] = {
    condition_data.name_cn: condition_data for condition_data in condition_data_base
}
