from sim.ability import *


def helloworld(self, field: SimpleField, **kwargs):
    side = field.sides[kwargs["org"][0]]
    for nonIndex in len(side.activeNons):
        nonIndex: int
        if nonIndex != kwargs["org"][1]:
            side.activeNons[nonIndex].statsLevel.ATK += 1
            targetName = side.activeNons[nonIndex].name
            field.log += "{}({})使得{}的攻击上升了一级……\n".format(
                side.activeNons[kwargs["org"][1]].name, self.reason, targetName
            )
    pass
    # field.
