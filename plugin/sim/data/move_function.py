from __future__ import annotations
from typing import TYPE_CHECKING
import random

if TYPE_CHECKING:
    from sim.field import Field


class MoveFunctions:
    """招式效果写在这里"""

    @staticmethod
    def may_burnt(
        field: Field, target_tuple: tuple[str, int], chance: float = 0.3, **kwargs
    ):
        if random.random() > chance:
            return
        target = field.tuple2non(target_tuple)
        target.add_condition("烧伤")
        field.log.append(f"{target.name}被烧伤了!")
