from __future__ import annotations
from typing import TYPE_CHECKING

from ..non_events import NonEvent


if TYPE_CHECKING:
    from sim.field import Field


class NonEventFunctions:
    """异常状态、特性、物品效果函数均写在这里"""

    @classmethod
    def helloWorld(cls, self: NonEvent, field: Field, **kwargs):
        side = field.sides[kwargs["org"][0]]
        for nonIndex in range(len(side.active_nons)):
            nonIndex: int
            if nonIndex != kwargs["org"][1] and side.active_nons[nonIndex].hp > 0:
                side.active_nons[nonIndex].stats_level.ATK += 1
                targetName = side.active_nons[nonIndex].name
                field.log.append(
                    "{}--[特性:{}]-->{}[ATK+1]".format(
                        side.active_nons[kwargs["org"][1]].name, self.reason, targetName
                    )
                )
                # field.log.append(
                #     "{}({})使得{}的攻击上升了一级……".format(
                #         side.activeNons[kwargs["org"][1]].name, self.reason, targetName
                #     )
                # )
        pass
        # field.

    @classmethod
    def burnt_end_of_turn(cls, self: NonEvent, field: Field, **kwargs):
        non = field.tuple2non(kwargs["org"])
        non.conditions["Burnt"].flags["turn"] += 1
        non.hp -= non.hp_max // 10

    @classmethod
    def noGlasses(cls, self: NonEvent, field: Field, **kwargs):
        orgNonTuple = kwargs["org"]
        orgNonTuple: tuple[str, int]
        field.sides[orgNonTuple[0]].commandList[
            orgNonTuple[1]
        ].targetTuple = field.ABC()  # ABC是写的随机获取一个目标的函数
