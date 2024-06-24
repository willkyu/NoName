from __future__ import annotations
from typing import TYPE_CHECKING

from ..non_events import NonEvent


if TYPE_CHECKING:
    from sim.field import Field


class ConditionFunctions:
    """异常状态、各种状态效果函数均写在这里"""

    @staticmethod
    def burnt_end_of_turn(cls, self: NonEvent, field: Field, **kwargs):
        non = field.tuple2non(kwargs["org"])
        non.conditions["烧伤"].flags["turn"] += 1
        field.log.append(
            f"{non.name}--[状态:{self.reason}]-->{non.name}[HP:{non.hp}-{non.hp_max//10}={max(0,non.hp-non.hp_max//10)}/{non.hp_max}]"
        )
        field.make_damage(kwargs["org"], non.hp_max // 10)
        # non.hp -= min(non.hp_max // 10, non.hp)

    @staticmethod
    def pollution_end_of_turn(cls, self: NonEvent, field: Field, **kwargs):
        non = field.tuple2non(kwargs["org"])
        non.conditions["污染"].flags["turn"] += 1
        turn = non.conditions["污染"].flags["turn"]
        field.log.append(
            f"{non.name}--[状态:{self.reason}({turn})]-->{non.name}[HP:{non.hp}-{non.hp_max//20*turn}={max(0,non.hp-non.hp_max//20*turn)}/{non.hp_max}]"
        )
        field.make_damage(kwargs["org"], non.hp_max // 20 * turn, non.hp)

        # non.hp -= min(non.hp_max // 20 * turn, non.hp)
