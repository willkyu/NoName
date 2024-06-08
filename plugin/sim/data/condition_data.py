from ..non_events import NonEventsObj
from ..condition import Condition
from .non_event_functions import NonEventFunctions

# baseCondition = []

conditionDataBase: list[Condition] = [
    Condition(
        name="Burnt",
        name_cn="烧伤",
        desc="烧伤不过百日长，你我都撑不起的未来，就让我来告别",
        flags={"turn": 0},
        add_non_events=NonEventsObj(end_of_turn=NonEventFunctions.burnt_end_of_turn),
    )
]
