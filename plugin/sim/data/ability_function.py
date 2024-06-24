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
        org_non_tuple = kwargs["org"]
        ally_list = field.get_ally_non(org_non_tuple)
        for non in ally_list:
            non.stats_level.ATK += 1
            field.log.append(
                f"{field.tuple2name(org_non_tuple)}--[特性:{self.reason}]-->{non.name}[ATK+1]"
            )

    @staticmethod
    def absolute_fairness(self: NonEvent, field: Field, **kwargs):
        org_non_tuple = kwargs["org"]

        all_non_list = field.get_all_non()
        for non in all_non_list:
            non.stats_level = field.generate_empty_stat_level()

        field.log.append(
            f"{field.tuple2name(org_non_tuple)}--[特性:{self.reason}]-->ALL[能力等级归零]"
        )

    @staticmethod
    def reborn(self: NonEvent, field: Field, **kwargs):
        org_non_tuple = kwargs["org"]
        died_ally_list = field.get_ally_non(org_non_tuple, alive=False)
        for target in died_ally_list:
            field.revive_non(target)
            field.log.append(
                f"{field.tuple2name(org_non_tuple)}--[特性:{self.reason}]-->{target.name}[HP:{target.hp}/{target.hp_max}]"
            )

    @staticmethod
    def water_stepping(self: NonEvent, field: Field, **kwargs):
        if field.weather == "Rainy":
            org_non = field.tuple2non(kwargs["org"])
            org_non.stats_level.SPE += 1
            field.log.append(f"{org_non.name}--[特性:{self.reason}]-->{org_non}[SPE+1]")

    @staticmethod
    def reluctant(self: NonEvent, field: Field, **kwargs):
        org_non_tuple = kwargs["org"]
        ally_list = field.get_ally_non(org_non_tuple)
        for non in ally_list:
            before, amount, after = field.recover(non, 0.125)
            field.log.append(
                f"{field.tuple2name(org_non_tuple)}--[特性:{self.reason}]-->{non.name}[HP:{before}+{amount}={after}/{non.hp_max}]"
            )

    @staticmethod
    def knee_jerk(self: NonEvent, field: Field, **kwargs):
        org_non = field.tuple2non(kwargs["org"])
        target_non = field.tuple2non(kwargs["move_org"])
        field.log.append(
            f"{org_non.name}--[特性:{self.reason}]-->{target_non.name}[HP:{target_non.hp}-{target_non.hp_max//8}={max(target_non.hp,0)}/{target_non.hp_max}]"
        )
        field.make_damage(kwargs["move_org"], target_non.hp_max // 8)
