import OlivOS
import os

# from typing import Literal

from .config import Config
from ..sim.field import get_non_entity
from ..sim.roll import gacha
from ..sim.global_utils import BASE_NON_FILE_PATH
from ..sim.data.living_area import area_data
from ..sim.player import Player


def config_update(user_id: str, cmd: str, config: Config, id: str = None):
    if user_id not in config.master_list:
        return
    match cmd:
        case "添加群":
            config.edit_config(id, "group", add_mode=True)
        case "移除群":
            config.edit_config(id, "group", add_mode=False)
        case "添加管理员":
            if user_id == "496373158":
                config.edit_config(id, "master", add_mode=True)
        case "移除管理员":
            if user_id == "496373158":
                config.edit_config(id, "master", add_mode=False)


def gacha_cmd(
    command_list: list[str],
    user_id: str,
    bot: OlivOS.API.Event,
    group_id: str = "",
):
    mode = "private" if group_id == "" else "group"
    if command_list[0].lower() != "gacha":
        return
    if len(command_list) == 1 or command_list[1] not in area_data.items():
        bot.send(
            mode,
            user_id if mode == "private" else group_id,
            message=f"请输入AREA:\n{list(area_data.items())}",
        )
        return
    if _check_temp_non(user_id):
        species_name = get_non_entity(user_id).species.name
        bot.send(
            mode,
            user_id if mode == "private" else group_id,
            message=f"暂存区中有未命名的NON({species_name})\n请先使用.non name 【NAME】对其命名.",
        )
    player = Player(user_id)
    bot.send(
        mode,
        user_id if mode == "private" else group_id,
        message=str(player),
    )
    gacha(player, command_list[1])


def name_cmd(
    command_list: list[str],
    user_id: str,
    bot: OlivOS.API.Event,
    group_id: str = "",
):
    mode = "private" if group_id == "" else "group"
    if command_list[0].lower() != "name" or len(command_list) < 2:
        return
    if len(command_list) == 2 and _check_temp_non(user_id):
        org_path = BASE_NON_FILE_PATH + f"{user_id}/TEMP.json"
        target_path = BASE_NON_FILE_PATH + f"{user_id}/NON/{command_list[1]}.json"
        if os.path.exists(target_path):
            non_species_name = get_non_entity(user_id, command_list[1]).species.name
            bot.send(
                mode,
                user_id if mode == "private" else group_id,
                message=f"已有名为{command_list[1]}的NON({non_species_name}).",
            )
            return

        non = get_non_entity(user_id)
        non.name = command_list[1]
        non.dump2json()
        os.remove(org_path)
        bot.send(
            mode,
            user_id if mode == "private" else group_id,
            message=f"已将暂存区的NON({non.species.name})取名为{command_list[1]}.",
        )
        return

    else:
        org_path = BASE_NON_FILE_PATH + f"{user_id}/NON/{command_list[1]}.json"
        target_path = BASE_NON_FILE_PATH + f"{user_id}/NON/{command_list[2]}.json"
        if not os.path.exists(org_path):
            bot.send(
                mode,
                user_id if mode == "private" else group_id,
                message=f"你没有名为{command_list[1]}的NON.",
            )
            return

        if os.path.exists(target_path):
            non_species_name = get_non_entity(user_id, command_list[2]).species.name
            bot.send(
                mode,
                user_id if mode == "private" else group_id,
                message=f"已有名为{command_list[2]}的NON({non_species_name}).",
            )
            return

        non = get_non_entity(user_id, command_list[1])
        non.name = command_list[2]
        non.dump2json()
        os.remove(org_path)
        bot.send(
            mode,
            user_id if mode == "private" else group_id,
            message=f"已将暂存区的NON({non.species.name})取名为{command_list[1]}.",
        )
        return


def _check_temp_non(user_id: str):
    return os.path.exists(path=BASE_NON_FILE_PATH + f"{user_id}/TEMP.json")
