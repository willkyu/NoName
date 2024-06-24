from __future__ import annotations
from json import load
import os
from random import shuffle, choice
import math
import random
from typing import Annotated, Callable, Literal

# import OlivOS

from .global_utils import (
    BattleMode,
    make_sure_dir,
    BASE_NON_FILE_PATH,
    id2name,
)
from .non import NON, MoveSlot, StatLevel
from .command import Command
from .player import Player
from .non_events import NonEventsObj


class Side:
    """每一个玩家是一个Side

    Returns:
        _type_: _description_
    """

    non_num: Literal[1, 2]  # 该规则下一次能出战几个NON
    active_nons: list[NON]  # 出战的NON
    not_active_nons: list[NON]  # 备战NON

    command_dict: dict[int, Command]  # {index, Command} index是出战NON的index

    # 一些其他的东西，如护盾
    shield: bool = False  # 己方全体护盾

    lose = False

    def __init__(self, team: list[NON], battle_mode: BattleMode) -> None:
        """给玩家的teamlist，战斗规则

        Args:
            team (list[NON]): _description_
            battleMode (BattleMode): _description_
        """
        self.non_num = 2 if battle_mode == "double" else 1
        self.active_nons, self.not_active_nons = (
            team[: self.non_num],
            team[self.non_num :],
        )
        self.command_dict = {i: None for i in range(self.non_num)}

    def add_command(self, index: int, command: Command) -> str | bool:
        """添加指令，如果成功返回True，否则是str，描述不合法原因

        Args:
            index (int): 指令的位置（哪个NON进行操作）
            command (Command): _description_

        Returns:
            str|bool: _description_
        """
        if index >= self.non_num or index < 0:
            return "指令对象超出范围"
        valid = self.check_command_valid(index, command)
        if isinstance(valid, str):
            return valid

        # 这里添加其他可能性

        pass
        self.command_dict[index] = command
        # print("{}已添加:\n{}\n".format(index, command))
        return True

    def check_command_valid(self, index: int, command: Command) -> str | bool:
        """检查指令合法性，如果合法返回True，否则是str，描述不合法原因

        Args:
            index (int): 指令的位置（哪个NON进行操作）
            command (Command): _description_

        Returns:
            str|bool: _description_
        """
        if command.action == "move" and command.move not in [
            move_slot for move_slot in self.active_nons[index].move_slots.keys()
        ]:
            return "无法使用该NON不会的招式"
        if self.active_nons[index].hp <= 0:
            return "该NON已昏厥"
        # 这之后可以再加别的检查合法性，比如不能交换状态进行交换
        return True

    def calculate_non_speed(self, command_index: int) -> int:
        # 计算指令的NON的当前速度
        non = self.active_nons[command_index]
        speed = (
            non.stat.SPA * (2 + non.stats_level.SPA) / 2
            if non.stats_level.SPA > 0
            else 2 / (2 - non.stats_level.SPA)
        )
        return speed
        pass

    def get_all_command(self) -> bool:
        """是否该Side的指令全部收到

        Returns:
            bool: _description_
        """

        if None in [
            self.command_dict[idx]
            for idx, non in enumerate(self.active_nons)
            if non.hp > 0
        ]:
            return False
        return True

    def check_lose(self):
        for non in self.active_nons:
            if non.hp > 0:
                return False
        self.lose = True
        return True

    pass


class Field:
    """包含战斗的各种信息

    Returns:
        _type_: _description_
    """

    sides: dict[str, Side]  # {userId: Side} 有哪几个玩家，分别对应一个Side
    non_team_dict: dict[str, list[NON]]  # {userId:[NON]} 玩家的队伍
    log: list[str]
    wait_switch_dict: dict[str, list[int]] = (
        None  # 用于存储是否需要等待用户换上NON，一般用于NON fainted之后，有些特殊技能也会用上
    )
    bot_send_group: Callable

    weather: str = "Normal"

    # 一些其他的东西
    last_used_move: str | None = None

    pass

    def __init__(
        self,
        player_list: Annotated[list[Player], "len should be 2 or 4"],
        battle_mode: BattleMode,
        log: list[str],
        bot_send_group: Callable,
    ) -> None:
        """初始化field

        Args:
            playerList (Annotated[list[Player], &quot;len should be 2 or 4&quot;]): 玩家id列表
            battleMode (BattleMode): 规则
            log (list[str]): log
        """
        self.non_team_dict = {
            player.id: [get_non_entity(player.id, non) for non in player.team]
            for player in player_list
        }
        self.sides = {
            player.id: Side(self.non_team_dict[player.id], battle_mode)
            for player in player_list
        }
        self.log = log
        self.bot_send_group = bot_send_group

        self.wait_switch_dict = {player_id: [] for player_id in self.sides.keys()}
        pass

    def exe_command(self, side_id: str, command_index: int):
        # * 注意，exe_command之前必须确保指令可行，也就是在add_command阶段就要检查指令可行性
        # * 执行指令，side_id与player_id是一个东西
        # do this command
        command: Command = self.sides[side_id].command_dict[command_index]

        if self.tuple2non((side_id, command_index)).hp <= 0:
            self.sides[side_id].command_dict[command_index] = None
            return

        match command.action:
            case "retire":
                # sideId输
                pass
            case "switch":
                target_non_index = command.target_tuple[1]
                self.event_trigger_single("before_switch", (side_id, command_index))
                self.log.append(
                    "{}收回了{}，派出了{}({}).".format(
                        id2name.get_name(side_id),
                        self.sides[side_id].active_nons[command_index].name,
                        command.target,
                        self.tuple2non(
                            command.target_tuple, active=False
                        ).species.name_cn,
                    )
                )

                # 交换
                (
                    self.sides[side_id].active_nons[command_index],
                    self.sides[side_id].not_active_nons[target_non_index],
                ) = (
                    self.sides[side_id].not_active_nons[target_non_index],
                    self.sides[side_id].active_nons[command_index],
                )
                self.event_trigger_single("on_active_once", (side_id, command_index))
            case "specialEvo":
                pass
            case "item":
                pass
            case "move":
                self.exe_move(side_id, command_index)
                pass
        self.sides[side_id].command_dict[command_index] = None
        pass
        # print(self.log)

    def exe_wait_switch(self, player_id: str, org_id: int, non_name: str):
        # 执行替补，一般是因为位置空了需要进行备战替补
        # orgId是需要换上的位置index，nonName是换上的NON的name

        if non_name not in [non.name for non in self.sides[player_id].not_active_nons]:
            return False
        target_non_index = self.get_non_tuple(non_name, player_id)[1]
        # self.eventTriggerSingle("beforeSwitch", (sideId, commandIndex))
        self.bot_send_group(
            "{}派出了{}到位置{}.".format(
                id2name.get_name(player_id),
                self.sides[player_id].not_active_nons[target_non_index].name,
                org_id,
            )
        )
        (
            self.sides[player_id].active_nons[org_id],
            self.sides[player_id].not_active_nons[target_non_index],
        ) = (
            self.sides[player_id].not_active_nons[target_non_index],
            self.sides[player_id].active_nons[org_id],
        )
        self.event_trigger_single("on_active_once", (player_id, org_id))
        return True

    def exe_move(self, side_id: str, command_index: int):
        # 执行move，比较复杂。还没写完
        command: Command = self.sides[side_id].command_dict[command_index]
        if command is None:
            return
        non = self.tuple2non((side_id, command_index))
        non.move_slots[command.move].pp -= 1
        target_tuple = command.target_tuple
        if command.target not in ["all"]:
            target_non = self.tuple2non(target_tuple)
            if target_non.hp <= 0:
                target_tuple = self.get_random_active_non_tuple(target_tuple[0])
                if not target_tuple:
                    self.log.append(f"{non.name}没有目标.")
                    return
                target_non = self.tuple2non(target_tuple)
            if target_non.battle_status.protect:
                self.log.append(f"{target_non.name}保护了自己.")
                return
        if non.move_slots[command.move].move.category != "Auxiliary":
            if command.target == "all":
                # TODO全体伤害
                pass
            # 伤害前效果
            non.move_slots[command.move].move.condition(
                self, target_tuple, org_tuple=(side_id, command_index)
            )

            damage = self.calculate_damage(
                non,
                non.move_slots[command.move],
                target_non,
            )
            self.log.append(
                "{}--[{}]-->{}[HP:{}-{}={}/{}]".format(
                    non.name,
                    command.move,
                    target_non.name,
                    target_non.hp,
                    damage,
                    max(target_non.hp - damage, 0),
                    target_non.hp_max,
                )
            )
            self.make_damage(target_tuple, damage)
            self.event_trigger_single(
                "on_hit", target_tuple, move_org=(side_id, command_index)
            )
            # 伤害后效果
            non.move_slots[command.move].move.secondary(
                self, target_tuple, org_tuple=(side_id, command_index)
            )

        else:
            # 辅助招式
            self.log.append(f"{non.name}使用了{command.move}.")
            non.move_slots[command.move].move.condition(
                self, target_tuple, org_tuple=(side_id, command_index)
            )

        pass

    def make_damage(self, non_tuple: tuple[str, int], damage: int):
        non_entity = self.tuple2non(non_tuple)
        if non_entity.hp <= 0:
            return
        non_entity.hp -= min(damage, non_entity.hp)
        if non_entity.hp <= 0:
            self.fainted_process(non_tuple)

    def recover(self, non: NON, amount: int | float):
        """恢复给定non的hp
            amount为回复量，如果为整数就是绝对值，如果为小数就是最大hp百分比

        Args:
            non (NON): _description_
            amount (int | float): _description_

        Returns:
            _type_: 回复前hp，回复的hp，回复后hp；用于log输出
        """
        if non.hp <= 0:
            return
        if isinstance(amount, float):
            if amount > 1 or amount < 0:
                return
            amount = math.floor(amount * non.hp_max)
        before, heal_amount = non.hp, amount
        amount = min(amount, non.hp_max - non.hp)
        non.hp += amount
        return before, heal_amount, non.hp

    def get_random_active_non_tuple(self, side_id=None):
        """获取一个随机的active的NON，不给sideId就从全局active的NON中选。
           现在有个问题是可能会选择自己

        Args:
            sideId (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        tuple_list = []
        if side_id is not None:
            for idx in range(self.sides[side_id].non_num):
                if self.tuple2non((side_id, idx), active=True).hp > 0:
                    tuple_list.append((side_id, idx))
        else:
            for side_id, side in self.sides.items():
                for idx in range(side.non_num):
                    if self.tuple2non((side_id, idx), active=True).hp > 0:
                        tuple_list.append((side_id, idx))
        if len(tuple_list) > 0:
            return choice(tuple_list)
        return False

    def fainted_process(self, target_tuple: tuple[str, int]):
        # fainted的处理
        self.log.append(
            "[{}]的[{}]倒下了……".format(
                id2name.get_name(target_tuple[0]), self.tuple2non(target_tuple).name
            )
        )
        if self.have_non_to_switch(target_tuple[0]):
            self.wait_switch_dict[target_tuple[0]].append(target_tuple[1])
            self.log.append(
                "{}将要选择NON到位置{}上.".format(
                    id2name.get_name(target_tuple[0]), target_tuple[1]
                )
            )
        elif self.sides[target_tuple[0]].check_lose():
            self.log.append(
                "{}没有可以拿出的NON了……".format(id2name.get_name(target_tuple[0]))
            )
        pass

    def calculate_damage(self, org_non: NON, move: MoveSlot, target_non: NON):
        # 计算伤害，orgNon是攻击方
        multiply = random.uniform(0.85, 1) * (
            1.5 if move.move.type in org_non.types else 1.0
        )
        category = move.move.category
        # TODO 计算属性克制倍率
        damage = multiply * (
            (2 * org_non.level + 10)
            / 250
            * (
                org_non.stat.ATK
                * (
                    (2 + org_non.stats_level.ATK) / 2
                    if org_non.stats_level.ATK > 0
                    else 2 / (2 - org_non.stats_level.ATK)
                )
                if category == "Physical"
                else org_non.stat.SPA
                * (
                    org_non.stat.SPA * (2 + org_non.stats_level.SPA) / 2
                    if org_non.stats_level.SPA > 0
                    else 2 / (2 - org_non.stats_level.SPA)
                )
            )
            / (
                target_non.stat.DEF
                * (
                    (2 + org_non.stats_level.DEF) / 2
                    if org_non.stats_level.DEF > 0
                    else 2 / (2 - org_non.stats_level.DEF)
                )
                if category == "Physical"
                else target_non.stat.SPD
                * (
                    (2 + org_non.stats_level.SPD) / 2
                    if org_non.stats_level.SPD > 0
                    else 2 / (2 - org_non.stats_level.SPD)
                )
            )
            * move.move.base_power
            + 2
        )

        return max(math.floor(damage), 1)

    def calculate_command_order(self):
        # 计算指令的顺序，同优先级下速度快的优先
        # commandDict: dict[tuple[str, int], Command] = {}
        command_list: list[tuple[list[tuple[str, int]], Command]] = []

        # 使用shuffle打乱顺序，实现相同速度下的随机排序

        for sideId, side in self.sides.items():
            for command_index, command in side.command_dict.items():
                if command is not None:
                    command_list.append([[sideId, command_index], command])
        shuffle(command_list)

        # calculate the order
        self.update_command_priority(command_list)
        command_priority_dict = {
            tuple(command_tuple): (
                command.priority if command is not None else 0,
                self.sides[command_tuple[0]].calculate_non_speed(command_tuple[1]),
            )
            for command_tuple, command in command_list
        }

        return [
            key
            for key, value in sorted(
                list(command_priority_dict.items()), key=lambda x: (-x[1][0], -x[1][1])
            )
        ]

    def calculate_speed_order(self, return_non_entity=False):
        # 计算指令的速度
        non_speed_list: list[list[list[str, int], NON]] = []

        # 使用shuffle打乱顺序，实现相同速度下的随机排序

        for side_id, side in self.sides.items():
            for non_idx in range(len(side.active_nons)):
                if self.tuple2non((side_id, non_idx)).hp > 0:
                    non_speed_list.append(
                        [[side_id, non_idx], side.calculate_non_speed(non_idx)]
                    )
        shuffle(non_speed_list)

        return_list = [
            tuple(key[0]) for key in sorted(non_speed_list, key=lambda x: (-x[1]))
        ]
        if return_non_entity:
            new_return_list = [self.tuple2non(non_tuple) for non_tuple in return_list]
            return [
                [return_list[i], new_return_list[i]] for i in range(len(return_list))
            ]
        return return_list

    def update_command_priority(
        self, command_list: list[tuple[list[tuple[str, int]], Command]]
    ) -> None:
        # 特殊情况下的优先级更新，比如追击
        pass

    def event_trigger_all(self, event_name: str, **kwargs):
        # 触发场上所有NON的名为eventName的nonEvent
        if not hasattr(NonEventsObj, event_name):
            return
        for non_tuple, non in self.calculate_speed_order(return_non_entity=True):
            kwargs.update({"org": non_tuple})
            exec("non.non_events.{}.exe(self,**kwargs)".format(event_name))

    def event_trigger_single(
        self, event_name: str, non_tuple: tuple[str, int], **kwargs
    ):
        # 触发指定NON的名为eventName的nonEvent
        if not hasattr(NonEventsObj, event_name):
            return
        non = self.tuple2non(non_tuple)  # noqa: F841
        kwargs.update({"org": non_tuple})
        exec("non.non_events.{}.exe(self,**kwargs)".format(event_name))

    def get_non_tuple(self, non_name: str, side_id: str = None):
        """给定一个non的名字，获取他的tuple。tuple可以理解为是该non的定位符。

        Args:
            nonName (str): _description_
            sideId (str, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        if side_id is None:
            for side_id, side in self.sides.items():
                for non_idx, non in enumerate(side.active_nons):
                    if non.name == non_name:
                        return (side_id, non_idx)
                for non_idx, non in enumerate(side.not_active_nons):
                    if non.name == non_name:
                        return (side_id, non_idx)
            return False
        else:
            for non_idx, non in enumerate(self.sides[side_id].active_nons):
                if non.name == non_name:
                    return (side_id, non_idx)
            for non_idx, non in enumerate(self.sides[side_id].not_active_nons):
                if non.name == non_name:
                    return (side_id, non_idx)
            return False

    def update_weather(self, weather: str, reason: str, org: tuple[str, int], **kwargs):
        # 尝试改变天气
        if self.weather == weather:
            self.log.append("天气没有任何变化……")
            return
        self.weather = weather
        self.log.append("由于[{}]天气变成了{}……".format(reason, self.weather))
        kwargs["weather_changed_org"] = org
        self.event_trigger_all("on_weather_changed", **kwargs)

    def get_ally_non(self, non_tuple: tuple[str, int], alive: bool = True) -> list[NON]:
        res_list = []
        for non_index in range(len(self.sides[non_tuple[0]])):
            non: NON = self.sides[non_tuple[0]].active_nons[non_index]
            if non_index != non_tuple[1] and (non.hp > 0 if alive else non.hp <= 0):
                res_list.append(non)
        return res_list

    def get_all_non(self) -> list[NON]:
        res_list = []
        for side in self.sides.values():
            for non_index in range(len(side.active_nons)):
                if side.active_nons[non_index].hp > 0:
                    res_list.append(side.active_nons[non_index])
        return res_list

    def revive_non(self, non: NON) -> None:
        if non.hp > 0:
            return
        non.hp = non.hp_max // 4
        non.stats_level = self.generate_empty_stat_level()

    def tuple2name(self, non_tuple: tuple) -> str:
        return self.tuple2non(non_tuple).name

    def tuple2non(self, non_tuple: tuple[str, int], active: bool = True):
        """给定一个non的tuple，返回该non对象。active用于指定他是否active

        Args:
            nonTuple (tuple[str, int]): _description_
            active (bool, optional): _description_. Defaults to True.

        Returns:
            _type_: _description_
        """
        if active:
            return self.sides[non_tuple[0]].active_nons[non_tuple[1]]
        return self.sides[non_tuple[0]].not_active_nons[non_tuple[1]]

    def have_non_to_switch(self, side_id: str):
        """给定一个sideId，判断他是否有能够换上来的备战NON

        Args:
            sideId (str): _description_

        Returns:
            _type_: _description_
        """
        for non in self.sides[side_id].not_active_nons:
            if non.hp > 0:
                # print(non.name)
                return True
        return False

    def generate_empty_stat_level(self):
        return StatLevel()


def get_non_entity(master_id: str, non_name: str = "") -> NON | bool:
    """从json获取NON实体

    Args:
        masterId (str): _description_
        nonName (str): _description_

    Returns:
        NON | bool: _description_
    """
    make_sure_dir(BASE_NON_FILE_PATH + "{}/NON/".format(master_id))
    path = BASE_NON_FILE_PATH + "{}/NON/{}.json".format(master_id, non_name)
    if non_name == "":
        path = BASE_NON_FILE_PATH + "{}/TEMP.json".format(master_id)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            non = NON(**load(f))
        # non.toEntity()
        return non
    else:
        # Oh fuck! It's impossible!
        return False
