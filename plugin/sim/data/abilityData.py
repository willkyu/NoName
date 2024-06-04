from sim.ability import *
from sim.data.nonEventFunctions import *

abilityDataBase: list[Ability] = [
    Ability(
        name="Hello World",
        cnName="你好世界",
        desc="出场时所有队友攻击等级+1",
        flags={},
        addNonEvents=NonEventsObj(
            onActiveOnce=NonEvent(reason="Hello World", exe=helloworld)
        ),
    )
]
