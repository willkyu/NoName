import random

from sim.ability import SimpleField


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


def noGlasses(self, field: SimpleField, **kwargs):
    orgNonTuple = kwargs["org"]
    field.sides[orgNonTuple[0]].commandList[
        orgNonTuple[1]
    ].targetTuple = field.ABC()  # ABC是写的随机获取一个目标的函数
