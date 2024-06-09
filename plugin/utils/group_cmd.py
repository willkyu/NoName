import OlivOS
from html import unescape

from .help_cmd import help_cmd
from .common_cmd import (
    config_update,
    gacha_cmd,
    name_cmd,
    give_cmd,
    team_cmd,
    info_cmd,
    use_cmd,
)
from .config import Config
from ..sim.battle import Battle
from ..sim.global_utils import battle_mode
from ..sim.data.item_data import item_data_dict_cn
from ..sim.player import Player

SELF_ID = "2136707662"


def unity_group_reply(
    plugin_event: OlivOS.API.Event,
    config: Config,
    bot_send: OlivOS.API.Event,
    group_battle_dict: dict[str, Battle],
):
    user_id: str = plugin_event.data.user_id
    group_id: str = plugin_event.data.group_id
    message: str = unescape(plugin_event.data.message)

    message = "." + message[1:] if message.startswith("。") else message

    if not message.lower().startswith(".non"):
        return

    if user_id not in [data["id"] for data in plugin_event.get_friend_list()["data"]]:
        bot_send.send("group", group_id, "请先添加为好友^^")

    group_command = message.lstrip(".non").strip().split(" ")
    match group_command[0]:
        case "开始战斗":
            if len(Player(user_id).team) < 1:
                bot_send.send("group", group_id, "你的队伍中没有成员.")
                return

            if (
                group_id in group_battle_dict
                and (not group_battle_dict[group_id].finished)
                and user_id in group_battle_dict[group_id].player_dict
            ):
                bot_send.send("group", group_id, "请不要重复参加.")
                return

            if len(group_command) < 2 and group_battle_dict.get(group_id, None) is None:
                bot_send.send(
                    "group", group_id, f"请选择战斗规则，可选项有:{battle_mode}"
                )
                return
            if (
                not group_battle_dict.get(group_id, False)
                and group_command[1] in battle_mode
            ) or (
                group_id in group_battle_dict and group_battle_dict[group_id].finished
            ):
                if group_command[1] == "double" and len(Player(user_id).team) < 2:
                    bot_send.send(
                        "group", group_id, "参加double战斗至少需要队伍中有两个NON."
                    )
                    return
                group_battle_dict[group_id] = Battle(
                    user_id, group_id, group_command[1], bot_send
                )
            elif group_battle_dict.get(group_id, False):
                if (
                    group_battle_dict.get(group_id).battle_mode == "double"
                    and len(Player(user_id).team) < 2
                ):
                    bot_send.send(
                        "group", group_id, "参加double战斗至少需要队伍中有两个NON."
                    )
                    return
                group_battle_dict[group_id].add_player(user_id)
                # if isinstance(addRes, dict):
                #     parserPatterns[groupId] = addRes
            else:
                bot_send.send(
                    "group", group_id, f"无此战斗规则，可选项有:{battle_mode}"
                )
            return
        case "添加群" | "移除群":
            config_update(user_id, group_command[0], config, group_id)
            return
        case "gift":
            if (
                len(group_command) < 2
                or group_command[1] not in item_data_dict_cn.keys()
            ):
                # print(list(item_data_dict_cn.keys()))
                return
            # print(bot_send.get_group_member_list(group_id))
            number = (
                int(group_command[2])
                if len(group_command) > 2 and group_command[2].isdigit()
                else 1
            )
            for player_info in bot_send.get_group_member_list(group_id)["data"]:
                player_id = player_info["id"]
                if player_id == SELF_ID:
                    continue
                player = Player(player_id)
                player.set_item(group_command[1], player.bag[group_command[1]] + number)
            bot_send.send(
                "group", group_id, f"已向所有群成员发放{group_command[1]}*{number}"
            )

    gacha_cmd(group_command, user_id, bot_send, group_id)
    name_cmd(group_command, user_id, bot_send, group_id)
    help_cmd(group_command, user_id, bot_send, group_id)
    give_cmd(group_command, user_id, bot_send, group_id)
    team_cmd(group_command, user_id, bot_send, group_id)
    use_cmd(group_command, user_id, bot_send, group_id)
    info_cmd(group_command, user_id, bot_send, group_id)
