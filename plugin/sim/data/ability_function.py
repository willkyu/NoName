from __future__ import annotations
from typing import TYPE_CHECKING

from ..non_events import NonEvent


if TYPE_CHECKING:
    from sim.field import Field


class AbilityFunctions:
    """特性效果函数均写在这里"""

    @classmethod
    def hello_world(cls, self: NonEvent, field: Field, **kwargs):
        side = field.sides[kwargs["org"][0]]
        for non_index in range(len(side.active_nons)):
            non_index: int
            if non_index != kwargs["org"][1] and side.active_nons[non_index].hp > 0:
                side.active_nons[non_index].stats_level.ATK += 1
                target_name = side.active_nons[non_index].name
                field.log.append(
                    "{}--[特性:{}]-->{}[ATK+1]".format(
                        side.active_nons[kwargs["org"][1]].name,
                        self.reason,
                        target_name,
                    )
                )
        pass
