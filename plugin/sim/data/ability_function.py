from __future__ import annotations
from typing import TYPE_CHECKING

from ..non_events import NonEvent


if TYPE_CHECKING:
    from sim.field import Field
    from ..non import StatLevel


class AbilityFunctions:
    """特性效果函数均写在这里"""

    @staticmethod
    def hello_world(self: NonEvent, field: Field, **kwargs):
        side = field.sides[kwargs["org"][0]]
        for non_index in range(len(side.active_nons)):
            if non_index != kwargs["org"][1] and side.active_nons[non_index].hp > 0:
                side.active_nons[non_index].stats_level.ATK += 1
                target_name = side.active_nons[non_index].name
                field.log.append(
                    f"{field.tuple2non(kwargs['org']).name}--[特性:{self.reason}]-->{target_name}[ATK+1]"
                )

    @staticmethod
    def absolute_fairness(self: NonEvent, field: Field, **kwargs):
        for side in field.sides.values():
            for non_index in range(len(side.active_nons)):
                if side.active_nons[non_index].hp > 0:
                    side.active_nons[non_index].stats_level = (
                        field.generate_empty_stat_level()
                    )

        field.log.append(
            f"{field.tuple2non(kwargs['org']).name}--[特性:{self.reason}]-->ALL[能力等级归零]"
        )

    @staticmethod
    def reborn(self: NonEvent, field: Field, **kwargs):
        for side in field.sides.values():
            for non_index in range(len(side.active_nons)):
                if side.active_nons[non_index].hp <= 0:
                    target = side.active_nons[non_index]
                    target.hp = target.hp_max // 2
                    target.stats_level = field.generate_empty_stat_level()
                    field.log.append(
                        f"{field.tuple2non(kwargs['org']).name}--[特性:{self.reason}]-->{target.name}[HP:{target.hp}/{target.hp_max}]"
                    )

    @staticmethod
    def water_stepping(self: NonEvent, field: Field, **kwargs):
        org_non = field.tuple2non(kwargs["org"])
        org_non.stats_level.SPE += 1
        field.log.append(f"{org_non.name}--[特性:{self.reason}]-->{org_non}[SPE+1]")

    @staticmethod
    def reluctant(self: NonEvent, field: Field, **kwargs):
        side = field.sides[kwargs["org"][0]]
        for non_index in range(len(side.active_nons)):
            if non_index != kwargs["org"][1] and side.active_nons[non_index].hp > 0:
                target = side.active_nons[non_index]
                recover = min(target.hp_max // 8, target.hp_max - target.hp)
                field.log.append(
                    f"{field.tuple2non(kwargs['org']).name}--[特性:{self.reason}]-->{target.name}[HP:{target.hp}+{target.hp_max//8}={target.hp+recover}/{target.hp_max}]"
                )
                target.hp += recover

    @staticmethod
    def knee_jerk(self: NonEvent, field: Field, **kwargs):
        org_non = field.tuple2non(kwargs["org"])
        target_non = field.tuple2non(kwargs["move_org"])
        field.log.append(
            f"{org_non.name}--[特性:{self.reason}]-->{target_non.name}[HP:{target_non.hp}-{target_non.hp_max//8}={max(target_non.hp,0)}/{target_non.hp_max}]"
        )
        field.make_damage(kwargs["move_org"], target_non.hp_max // 8)
