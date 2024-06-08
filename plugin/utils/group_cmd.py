import OlivOS
from html import unescape

from .common_cmd import config_update, gacha_cmd, name_cmd
from .config import Config
from ..sim.battle import Battle
from ..sim.global_utils import battle_mode


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
            if len(group_command) < 2 and group_battle_dict.get(group_id, None) is None:
                bot_send.send(
                    "group", group_id, "请选择战斗规则，可选项有:{}".format(battle_mode)
                )
            if (
                not group_battle_dict.get(group_id, False)
                and group_command[1] in battle_mode
            ) or (
                group_id in group_battle_dict and group_battle_dict[group_id].finished
            ):
                group_battle_dict[group_id] = Battle(
                    user_id, group_id, group_command[1], bot_send
                )
            elif group_battle_dict.get(group_id, False):
                group_battle_dict[group_id].add_player(user_id)
                # if isinstance(addRes, dict):
                #     parserPatterns[groupId] = addRes
            else:
                bot_send.send(
                    "group", group_id, "无此战斗规则，可选项有:{}".format(battle_mode)
                )
            return
        case "添加群" | "移除群":
            config_update(user_id, group_command[0], config, group_id)
            return

    gacha_cmd(group_command, user_id, bot_send, group_id)
    name_cmd(group_command, user_id, bot_send, group_id)
