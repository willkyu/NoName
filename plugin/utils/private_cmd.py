import OlivOS
from html import unescape

from .common_cmd import gacha_cmd, name_cmd, config_update
from .config import Config
from ..sim.battle import Battle


def unity_private_reply(
    plugin_event: OlivOS.API.Event,
    config: Config,
    bot_send: OlivOS.API.Event,
    group_battle_dict: dict[str, Battle],
):
    user_id: str = plugin_event.data.user_id
    # groupId: str = plugin_event.data.group_id
    message: str = unescape(plugin_event.data.message)

    message = "." + message[1:] if message.startswith("。") else message

    if not message.lower().startswith(".non"):
        return

    group_id = False
    for group_id_ in group_battle_dict:
        if user_id in group_battle_dict[group_id_].player_dict:
            group_id = group_id_
            break

    user_command = message[4:].strip().split(" ")

    if user_command[0] in ["0", "1", "2", "3", "4", "q"]:
        if not group_id:
            bot_send.send("private", user_id, "你未参加任何战斗.")
        elif user_id in group_battle_dict[group_id].player_command_processors.keys():
            group_battle_dict[group_id].add_command(user_id, user_command)
        else:
            bot_send.send("private", user_id, "无需发出指令.")
        return
    if (
        user_command[0] in ["添加群", "移除群", "添加管理员", "移除管理员"]
        and len(user_command) > 1
    ):
        config_update(user_id, user_command[0], config, user_command[1])

    gacha_cmd(user_command, user_id, bot_send)
    name_cmd(user_command, user_id, bot_send)
