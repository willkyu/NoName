from __future__ import annotations
from typing import TYPE_CHECKING

from ..non_events import NonEvent


if TYPE_CHECKING:
    from sim.field import Field


class ItemFunctions:
    """物品效果函数均写在这里"""

    @classmethod
    def infinite_pitaya_on_hit(cls, self: NonEvent, field: Field, **kwargs):
        """无限火龙果：每次被攻击后恢复最大HP的1/10."""
        self_tuple = kwargs["org"]
        non = field.tuple2non(self_tuple)
        recover_hp = min(non.hp_max // 10, non.hp_max - non.hp)
        field.log.append(
            f"{non.name}--[物品:{self.reason}]-->{non.name}[HP:{non.hp}+{non.hp_max//10}={non.hp+recover_hp}/{non.hp_max}]"
        )
        non.hp += recover_hp
