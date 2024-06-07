from sim.condition import *
from sim.data.nonEventFunctions import *

# baseCondition = []

conditionDataBase: list[Condition] = [
    Condition(
        name="Burnt",
        cnName="烧伤",
        desc="烧伤不过百日长，你我都撑不起的未来，就让我来告别",
        flags={"turn": 0},
        addNonEvents=NonEventsObj(endOfTurn=burntEndOfTurn),
    )
]
