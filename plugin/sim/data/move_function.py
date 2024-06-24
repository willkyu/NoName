from __future__ import annotations
from typing import TYPE_CHECKING
import random

if TYPE_CHECKING:
    from sim.field import Field


class MoveFunctions:
    """招式效果写在这里"""

    @staticmethod
    def may_burnt(
        field: Field, non_tuple: tuple[str, int], chance: float = 0.3, **kwargs
    ):
        if random.random() > chance:
            return
        non = field.tuple2non(non_tuple)
        non.add_condition("烧伤")
        field.log.append(f"{non.name}被烧伤了!")

    @staticmethod
    def may_pollution(
        field: Field, non_tuple: tuple[str, int], chance: float = 0.3, **kwargs
    ):
        if random.random() > chance:
            return
        non = field.tuple2non(non_tuple)
        if "污染" not in non.conditions:
            non.add_condition("污染")
            field.log.append(f"{non.name}受到了污染!")
        else:
            non.conditions["污染"].flags["turn"] += 1
            field.log.append(f"{non.name}的污染加重了!")

    @staticmethod
    def may_pollution_all(
        field: Field, non_tuple: tuple[str, int], chance: float = 0.3, **kwargs
    ):
        non = field.tuple2non(kwargs["org"])
        all_non_list = field.get_all_non()
        for non in all_non_list:
            if random.random() > chance:
                continue
            if "污染" not in non.conditions:
                non.add_condition("污染")
                field.log.append(f"{non.name}受到了污染!")
            else:
                non.conditions["污染"].flags["turn"] += 1
                field.log.append(f"{non.name}的污染加重了!")

    @staticmethod
    def protect(field: Field, non_tuple: tuple[str, int], chance: float = 1, **kwargs):
        non = field.tuple2non(kwargs["org"])
        non.battle_status.protect = True
        field.log.append(f"{non.name}准备保护自己.")

    @staticmethod
    def pray_for_rain(
        field: Field, non_tuple: tuple[str, int] | str, chance: float = 1, **kwargs
    ):
        field.update_weather("Rainy", "招式:祈雨", org=kwargs["org"])
