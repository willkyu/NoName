from __future__ import annotations
from typing import TYPE_CHECKING

from ..non_events import NonEvent


if TYPE_CHECKING:
    from sim.field import Field


class ItemFunctions:
    """物品效果函数均写在这里"""

    @staticmethod
    def infinite_pitaya_on_hit(cls, self: NonEvent, field: Field, **kwargs):
        """无限火龙果：每次被攻击后恢复最大HP的1/10."""
        self_tuple = kwargs["org"]
        non = field.tuple2non(self_tuple)
        if non.hp < 0:
            return
        before, amount, after = field.recover(non, 0.1)
        field.log.append(
            f"{non.name}--[物品:{self.reason}]-->{non.name}[HP:{before}+{amount}={after}/{non.hp_max}]"
        )
