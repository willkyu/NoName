from __future__ import annotations
import math
from typing import TYPE_CHECKING

from sim.ability import *

# if TYPE_CHECKING:
#     from sim.field import


def helloWorld(self: NonEvent, field: Field, **kwargs):
    side = field.sides[kwargs["org"][0]]
    for nonIndex in range(len(side.activeNons)):
        nonIndex: int
        if nonIndex != kwargs["org"][1] and side.activeNons[nonIndex].hp > 0:
            side.activeNons[nonIndex].statsLevel.ATK += 1
            targetName = side.activeNons[nonIndex].name
            field.log.append(
                "{}--[特性:{}]-->{}[ATK+1]".format(
                    side.activeNons[kwargs["org"][1]].name, self.reason, targetName
                )
            )
            # field.log.append(
            #     "{}({})使得{}的攻击上升了一级……".format(
            #         side.activeNons[kwargs["org"][1]].name, self.reason, targetName
            #     )
            # )
    pass
    # field.


def burntEndOfTurn(self, field: Field, **kwargs):
    non = field.tuple2Non(kwargs["org"])
    non.conditions["Burnt"].flags["turn"] += 1
    non.hp -= non.hpmax // 10
