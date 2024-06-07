from ..ability import *
from .nonEventFunctions import *

abilityDataBase: list[Ability] = [
    Ability(
        name="Hello World",
        cnName="你好世界",
        desc="出场时所有队友攻击等级+1",
        flags={},
        addNonEvents=NonEventsObj(
            onActiveOnce=[NonEvent(reason="Hello World", exe=helloWorld)]
        ),
    )
]


abilityDataDictEn: dict[str, Ability] = {
    abilityData.name: abilityData for abilityData in abilityDataBase
}

abilityDataDictCn: dict[str, Ability] = {
    abilityData.cnName: abilityData for abilityData in abilityDataBase
}
