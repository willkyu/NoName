from dataclasses import dataclass
from typing import Literal

from .data.move_data import move_data_dict_en


@dataclass
class Command:
    target: str | None
    action: Literal["switch", "retire", "specialEvo", "move", "item"]
    move: str | None
    priority: int = 0
    target_tuple: tuple[str, int] = None

    def __post_init__(self):
        if self.action == "move":
            self.priority = get_move_priority(self.move)
        else:
            self.priority = 10


def get_move_priority(move: str) -> int:
    return move_data_dict_en[move].priority
    pass
