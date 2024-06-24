from __future__ import annotations
from dataclasses import dataclass
from typing import Literal
import math
import OlivOS

from .global_utils import BattleMode, id2name, write_coin
from .field import Field, get_non_entity
from .player import Player
from .command import Command
from .non import NonTempBattleStatus


class log(list):
    def append(self, object: object) -> None:
        print(str(object))
        return super().append(object)


class Battle:
    group_id: str
    turn: int
    field: Field
    player_dict: dict[str, Player]  # {qqId: Player}
    promoter_id: str  # 发起人
    battle_mode: BattleMode
    log: list[str]
    player_num: int
    bot: OlivOS.API.Event  # bot messager
    non_name_list: list[str]
    ready4commands: bool = False
    finished: bool = False  # For test
    player_command_processors: dict[str, CommandProcessor] = {}

    def __init__(
        self,
        player_id: str,
        group_id: str,
        battle_mode: BattleMode,
        bot: OlivOS.API.Event,
    ) -> None:
        """注意，当你实例化Battle的时候，说明你已经检查过groupId下没有其他的Battle实例."""
        self.group_id = group_id
        self.non_name_list = []
        self.bot = bot
        self.ready4commands = False
        self.player_dict = {}
        self.finished = False
        self.promoter_id = player_id
        self.player_dict[player_id] = Player(player_id)
        self.non_name_list += self.player_dict[player_id].team
        # self.playerIdList.append(playerId)
        self.battle_mode = battle_mode
        self.log = []
        self.player_num = 4 if self.battle_mode == "chaos4" else 2
        self.send_group(
            "[{}]发出了对战邀请，当前状态：{}/{}".format(
                id2name.get_name(player_id),
                len(self.player_dict),
                self.player_num,
            )
        )
        pass

    def add_player(self, player_id: str):
        """添加玩家，成功True，失败False

        Args:
            playerId (str): _description_

        Returns:
            _type_: _description_
        """
        if len(self.player_dict) >= self.player_num:
            return False
        can_add = self.can_add_player(player_id)
        if isinstance(can_add, str):
            self.send_group(
                "[{}]想要接受对战邀请，但是{}.".format(
                    id2name.get_name(player_id), can_add
                ),
                log=False,
            )
            return False
        self.player_dict[player_id] = Player(player_id)
        self.non_name_list += self.player_dict[player_id].team
        if len(self.player_dict) == self.player_num:
            self.send_group(
                "[{}]接受了对战邀请，当前状态：{}/{}\n即将开始对战...".format(
                    id2name.get_name(player_id),
                    len(self.player_dict),
                    self.player_num,
                )
            )
            self.start()
            # parserPattern = {
            #     "action": ["switch", "retire", "specialEvo", "move", "item"],
            #     "nonName": self.nonNameList,
            # }
            # return parserPattern
        else:
            self.send_group(
                "[{}]接受了对战邀请，当前状态：{}/{}".format(
                    id2name.get_name(player_id),
                    len(self.player_dict),
                    self.player_num,
                )
            )
        return True

    def call_for_commands(self):
        """首先检查是否决出胜负，否则向所有玩家发送 请输入指令"""
        not_lose_side_list = [
            side_id for side_id, side in self.field.sides.items() if not side.lose
        ]
        if len(not_lose_side_list) > 1:
            self.player_command_processors = {
                playerId: None for playerId in self.player_dict.keys()
            }
            for playerId in self.player_dict.keys():
                self.player_command_processors[playerId] = CommandProcessor(
                    self.field, playerId, self.bot
                )
                # self.sendPrivate(playerId, "请输入指令.")
            self.ready4commands = True
        elif len(not_lose_side_list) == 1:
            self.end(winner_id=not_lose_side_list[0])
        else:
            self.send_group("DRAW! NO WINNER!")
            self.finished = True
            self.set_inbattle(False)

    def start(self):
        self.set_inbattle()
        self.player_command_processors = {
            player_id: None for player_id in self.player_dict.keys()
        }

        """战斗开始"""
        self.field = Field(
            self.player_dict.values(), self.battle_mode, self.log, self.send_group
        )
        start_battle_message = "————————————\n▼ 战斗开始！\n┣———————————\n"
        for player_id in self.player_dict.keys():
            start_battle_message += "▶ 玩家[{}]派出了[{}]({}){}\n".format(
                id2name.get_name(player_id),
                self.field.sides[player_id].active_nons[0].name,
                self.field.sides[player_id].active_nons[0].species.name_cn,
                (
                    ""
                    if self.battle_mode != "double"
                    else "与[{}]({})".format(
                        self.field.sides[player_id].active_nons[1].name,
                        self.field.sides[player_id].active_nons[1].species.name_cn,
                    )
                ),
            )
        start_battle_message += "————————————"
        # for player in self.playerDict.keys():
        #     for non in self.field.sides[player].activeNons:
        #         non.inBattle = self.groupId
        #         non.save()
        #     for non in self.field.sides[player].notActiveNons:
        #         non.inBattle = self.groupId
        #         non.save()
        self.send_group(start_battle_message)
        self.field.event_trigger_all("on_active_once")
        self.send_group("\n".join(self.log))
        self.log.clear()
        self.turn = 0
        self.call_for_commands()

    def set_inbattle(self, inbattle: bool = True):
        for player_id in self.player_dict.keys():
            for non_name in Player(player_id).team:
                non = get_non_entity(player_id, non_name)
                non.in_battle = self.group_id if inbattle else ""
                non.save()

    def each_turn(self):
        """每回合的操作"""
        self.turn += 1
        for side_id, side in self.field.sides.items():
            for index in range(len(side.active_nons)):
                non = self.field.tuple2non((side_id, index))
                non.battle_status = NonTempBattleStatus()
        self.send_group(
            "===============\nTurn {} Start!\n===============".format(self.turn)
        )
        command_list_this_turn = self.field.calculate_command_order()
        for command_tuple in command_list_this_turn:
            # self.log.append("执行command:\n" + str(commandTuple))
            self.field.exe_command(*command_tuple)

        # 回合结束处理
        self.field.event_trigger_all("end_of_turn")

        # print(self.log)
        self.send_group("\n".join(self.log))
        self.log.clear()
        self.send_group(
            "===============\nTurn {} End!\n===============".format(self.turn)
        )

        wait_switch_flag = False
        # 检查所有fainted的NON
        for player_id, fainted_list in self.field.wait_switch_dict.items():
            if len(fainted_list) > 0:
                self.player_command_processors[player_id] = CommandProcessor(
                    self.field,
                    player_id,
                    self.bot,
                    wait_switch_mode=True,
                )
                wait_switch_flag = True
                self.ready4commands = False

        if not wait_switch_flag:
            self.send_group("\n".join(self.log))
            self.log.clear()
            self.call_for_commands()
        pass

    def end(self, winner_id: str):
        """battle结束，胜负已分

        Args:
            winnerId (str): _description_
        """
        self.finished = True
        self.set_inbattle(False)

        loser_list = [
            player for player in self.player_dict.keys() if player != winner_id
        ]
        bonus = 0
        for lose in loser_list:
            write_coin(lose, Player(lose).coin - 50)
            bonus += 50
        bonus = math.floor(bonus * 0.8)
        write_coin(winner_id, Player(winner_id).coin + bonus)
        self.send_group(
            f"WINNER is {id2name.get_name(winner_id)}! 获得了{bonus}点灵魂，其他人失去了50点灵魂."
        )

        pass

    def add_command(self, player_id: str, com: str):
        """添加指令

        Args:
            playerId (str): _description_
            com (str): _description_
        """

        self.player_command_processors[player_id].get_command(com)
        if self.player_command_processors[player_id].wait_switch_mode:
            wait_switch_flag = False
            for _, fainted_list in self.field.wait_switch_dict.items():
                if len(fainted_list) > 0:
                    wait_switch_flag = True
            if wait_switch_flag:
                return
            self.send_group("\n".join(self.log))
            self.log.clear()
            self.call_for_commands()
        elif self.get_all_command():
            self.player_command_processors = {
                player_id: None for player_id in self.player_dict.keys()
            }
            self.each_turn()

    def get_all_command(self) -> bool:
        """检查是否收到所有指令

        Returns:
            bool: _description_
        """
        for side in self.field.sides.values():
            if not side.get_all_command():
                return False
        return True

    def send_group(self, message: str, log=False):
        if message.strip() == "":
            return
        # 发送群聊消息并记入log
        if not isinstance(message, str):
            return
        if log:
            self.log.append(message)
        self.bot.send("group", self.group_id, message)

    def send_private(self, player_id: str, message: str):
        # 发送私聊消息，不记入log
        if not isinstance(message, str):
            return
        self.bot.send("private", player_id, message)

    def can_add_player(self, player_id: str):
        """检查player是否可以参加这场战斗，比如检查队伍内是否有在battle中的NON

        Args:
            playerId (str): _description_

        Returns:
            _type_: _description_
        """
        player = Player(player_id)
        for non_name in player.team:
            if get_non_entity(player_id, non_name).in_battle != "":
                return "队伍中已有NON处于对战状态"
        for non_name in player.team:
            if non_name in self.non_name_list:
                return "{}与战斗中已有NON重名".format(non_name)
        return True


@dataclass
class CommandProcessor:
    field: Field
    player_id: str
    bot: OlivOS.API.Event
    wait_switch_mode: bool = False

    current_non: str = None
    non_name_list: list[str] = None
    command_pieces: dict[str, list] = None
    # commandList: list[str] = []
    int2str: dict[int, str] = None

    def __post_init__(self):
        self.side = self.field.sides[self.player_id]
        self.non_name_list = (
            [non.name for non in self.side.active_nons if non.hp > 0]
            if not self.wait_switch_mode
            else [non.name for non in self.side.active_nons if non.hp <= 0]
        )
        self.command_pieces = {non_name: [] for non_name in self.non_name_list}
        self.current_non = self.non_name_list[0]
        self.int2str = {}
        self.command_overall_hint()
        self.send(self.hint())

    def get_command(self, com: Literal["0", "1", "2", "3", "4", "q"]):
        if com not in set([str(key) for key in self.int2str.keys()] + ["q"]) & set(
            ["0", "1", "2", "3", "4", "q"]
        ):
            self.send("无此指令.")
            return

        if com == "q":
            # 清空当前NON已存命令
            self.command_pieces[self.current_non].clear()
            self.send(self.hint())
            return

        # 添加命令
        com = int(com)

        if self.wait_switch_mode:
            index = self.field.get_non_tuple(self.current_non)[1]
            self.field.exe_wait_switch(self.player_id, index, self.int2str[com])
            self.field.wait_switch_dict[self.player_id].remove(index)

            self.send("已收到替补{}(位置{})的指令.".format(self.int2str[com], index))

            self.get_next_non_name()

        elif self.current_non is None:
            self.send("当前无需指令.")

        elif len(self.command_pieces[self.current_non]) == 0:
            if self.int2str[com].startswith("move"):
                self.command_pieces[self.current_non].append("move")
                self.command_pieces[self.current_non].append(self.int2str[com][4:])
            elif self.int2str[com] == "switch":
                self.command_pieces[self.current_non].append("switch")
                self.command_pieces[self.current_non].append("")

        elif len(self.command_pieces[self.current_non]) == 2:
            self.command_pieces[self.current_non].append(self.int2str[com])
            # 该Command完成了
            index = self.field.get_non_tuple(self.current_non, self.player_id)[1]
            com_list = self.command_pieces[self.current_non]
            command = Command(com_list[2], com_list[0], com_list[1])
            command.target_tuple = self.field.get_non_tuple(command.target)
            res = self.field.sides[self.player_id].add_command(index, command)

            if isinstance(res, str):
                self.send(res)
            else:
                self.send("已收到{}的指令.".format(self.current_non))
                self.get_next_non_name()

        self.send(self.hint())

    def get_next_non_name(self):
        self.non_name_list = self.non_name_list[1:]
        if len(self.non_name_list) > 0:
            self.current_non = self.non_name_list[0]
        else:
            self.current_non = None
        pass

    def hint(self):
        if self.current_non is None:
            return ""

        if self.wait_switch_mode:
            self.int2str.clear()
            index = self.field.get_non_tuple(self.current_non)[1]
            hint_str = "请选择替换{}(位置{})的NON:\n".format(self.current_non, index)

            switch_list = []
            for idx, non in enumerate(self.side.not_active_nons):
                if non.hp <= 0:
                    continue
                switch_list.append(non.name)
            for idx, non in enumerate(switch_list):
                self.int2str[idx] = non
                hint_str += "指令【.non {}】:{}\n".format(idx, non)
            return hint_str

        if len(self.command_pieces[self.current_non]) == 0:
            non = self.get_current_non_entity()
            self.int2str.clear()
            hint_str = "请选择{}的行动:\n".format(self.current_non)
            for idx, move_slot in enumerate(list(non.move_slots.values())):
                if move_slot.pp <= 0:
                    continue
                self.int2str[idx] = "move" + move_slot.name_cn
                hint_str += "指令【.non {}】:{}\n".format(idx, move_slot.name_cn)
            if self.can_switch():
                hint_str += "指令【.non {}】:{}".format(len(self.int2str), "switch")
                self.int2str[len(self.int2str)] = "switch"
            return hint_str

        if len(self.command_pieces[self.current_non]) == 2:
            match self.command_pieces[self.current_non][0]:
                case "switch":
                    hint_str = "请选择交换的目标:\n"
                    self.int2str.clear()
                    switch_list = []
                    for idx, non in enumerate(self.side.not_active_nons):
                        if non.hp <= 0:
                            continue
                        switch_list.append(non.name)
                    for idx, non in enumerate(switch_list):
                        self.int2str[idx] = non
                        hint_str += "指令【.non {}】:{}\n".format(idx, non)
                    hint_str += "指令【.non {}】:{}".format("q", "重新选择")
                    return hint_str
                case "move":
                    hint_str = "请选择{}的目标:\n".format(
                        self.command_pieces[self.current_non][1]
                    )
                    non = self.get_current_non_entity()
                    self.int2str.clear()

                    target_list = []
                    match non.move_slots[
                        self.command_pieces[self.current_non][1]
                    ].move.target:
                        case "normal":
                            for sideId, side in self.field.sides.items():
                                if sideId == self.player_id:
                                    continue
                                target_list += [
                                    (non_target.name, sideId)
                                    for non_target in side.active_nons
                                    if non_target.hp > 0
                                ]
                            target_list += [
                                (non_target.name, self.player_id)
                                for non_target in self.side.active_nons
                                if non_target.hp > 0
                                and non_target.name != self.current_non
                            ]
                        case "all":
                            target_list += ["all"]
                    for idx, non_name in enumerate(target_list):
                        if not isinstance(non_name, tuple):
                            self.int2str[idx] = non_name
                            hint_str += "指令【.non {}】:{}\n".format(idx, non_name)
                            continue
                        self.int2str[idx] = non_name[0]
                        hint_str += "指令【.non {}】:{}({})\n".format(
                            idx, non_name[0], id2name.get_name(non_name[1])
                        )
                    hint_str += "指令【.non {}】:{}".format("q", "重新选择")
                    return hint_str
                case _:
                    return "意外的错误！或是{}未实现.".format(
                        self.command_pieces[self.current_non][0]
                    )

    def get_current_non_entity(self):
        return self.field.tuple2non(
            self.field.get_non_tuple(self.current_non, self.player_id)
        )

    def can_switch(self):
        return self.field.have_non_to_switch(self.player_id)

    def command_overall_hint(self):
        if self.wait_switch_mode:
            return

        # side = self.field.sides[self.playerId]
        hint = "当前Active的NON有:\n"
        for non in self.side.active_nons:
            hint += "{}[{}]({}) HP:{}/{} Level:{}, w.\n".format(
                "×" if non.hp <= 0 else "",
                non.name,
                non.species.name_cn,
                non.hp,
                non.hp_max,
                non.level,
            )
            for move_slot in non.move_slots.values():
                hint += "·{}({}) Type:{} pp:{}/{}\n".format(
                    move_slot.name_cn,
                    move_slot.move.category,
                    move_slot.move.type,
                    move_slot.pp,
                    move_slot.pp_max,
                )
            hint += "==========\n"
        hint += "备战NON有:{}".format(
            [
                "{}".format("×" if non.hp <= 0 else "") + non.name
                for non in self.side.not_active_nons
            ]
        )
        self.send(hint)

    def send(self, message: str):
        if message == "":
            return
        self.bot.send("private", self.player_id, message)
        # for non in side.notActiveNons:
