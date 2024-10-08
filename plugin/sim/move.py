from dataclasses import dataclass
from typing import Callable, Literal


SpecialEffectClass = Callable | str | None  # 特殊效果，还没想好是函数还是字符串


@dataclass
class MoveData:
    """招式数据类型，不是具体绑定在NON身上的招式"""

    id: int
    # 招式名
    name: str
    name_cn: str
    # 使用次数
    pp: int
    # 类型，物理魔法辅助
    category: Literal["Physical", "Magical", "Auxiliary"]
    # 属性，水火草这种
    type: str
    # 目标范围
    target: Literal[
        "adjacentAlly",  # 相邻队友
        "adjacentAllyOrSelf",  # 相邻队友或自身
        "adjacentFoe",  # 相邻敌方
        "all",  # 所有或是影响field
        "allAdjacent",  # 相邻所有
        "allAdjacentFoes",  # 相邻所有敌方
        "allies",  # 所有在场队友
        "allySide",  # 队友侧
        "allyTeam",  # 队友（包括不在场队友，不包括fainted的）
        "any",  # 任意一个
        "foeSide",  # 敌方侧
        "normal",  # 任意一个相邻
        "randomNormal",  # 随机一个相邻
        "scripted",  # 反伤
        "self",  # 自己
    ]
    # description
    desc: str
    # 用于随机技能
    can_be_rolled: bool = True
    # 一些特殊效果before use，还没想好是函数还是字符串
    condition: SpecialEffectClass | None = None
    # 基础伤害
    base_power: int | None = None
    # 基础命中，如果为True就是必中技能，如果为False就是要实时计算的
    accuracy: bool | int = True
    # 先制度
    priority: int = 0
    # 一些布尔型flag，比如是否能突破保护
    flags: dict[str, bool] | None = None
    # 招式附加效果after use
    secondary: SpecialEffectClass | None = None
    # 是否固定伤害值
    damage: None | int | Literal["level"] = None

    # one hit knockout，str是免疫的属性
    ohko: bool | str = False

    # TODO
    pass

    def __post_init__(self):
        if self.condition is None:
            self.condition = do_nothing
        if self.secondary is None:
            self.secondary = do_nothing

    def __str__(self):
        move_str = ""
        move_str += f"{self.name_cn} {self.name}({self.category}) Type: {self.type} pp: {self.pp}\n"
        if self.base_power is not None:
            move_str += f"Base Power: {self.base_power}"
        move_str += "Accuracy: {}\n".format(
            "--" if isinstance(self.accuracy, bool) else self.accuracy
        )
        move_str += self.desc
        return move_str


def do_nothing(field, target_tuple, **kwargs):
    pass
