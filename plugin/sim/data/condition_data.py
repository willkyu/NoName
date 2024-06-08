from ..non_events import NonEventsObj
from ..condition import Condition
from .condition_function import ConditionFunctions

# baseCondition = []

condition_data_base: list[Condition] = [
    Condition(
        name="Burnt",
        name_cn="烧伤",
        desc="烧伤不过百日长，你我都撑不起的未来，就让我来告别",
        flags={"turn": 0},
        add_non_events=NonEventsObj(end_of_turn=ConditionFunctions.burnt_end_of_turn),
    )
]
