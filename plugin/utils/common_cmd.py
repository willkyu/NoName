import OlivOS
import os
import json

# from typing import Literal

from .config import Config
from ..sim.field import get_non_entity
from ..sim.roll import gacha
from ..sim.global_utils import BASE_NON_FILE_PATH, id2name
from ..sim.data.living_area import area_data
from ..sim.player import Player
from ..sim.data.item_data import item_data_dict_cn
from ..sim.data.species_data import species_data_dict_cn
from ..sim.data.condition_data import condition_data_dict_cn
from ..sim.data.ability_data import ability_data_dict_cn
from ..sim.data.move_data import move_data_dict_cn


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
    if len(command_list) == 1 or command_list[1] not in area_data.keys():
        bot.send(
            mode,
            user_id if mode == "private" else group_id,
            message=f"请输入AREA:\n{list(area_data.keys())}",
        )
        return
    if _check_temp_non(user_id):
        species_name = get_non_entity(user_id).species.name_cn
        bot.send(
            mode,
            user_id if mode == "private" else group_id,
            message=f"{id2name.get_name(user_id)}的暂存区中有未命名的NON({species_name})\n请先使用.non name 【NAME】对其命名.",
        )
        return
    player = Player(user_id)
    bot.send(
        mode,
        user_id if mode == "private" else group_id,
        message=str(player),
    )
    gacha_res = gacha(player, command_list[1])
    if not gacha_res:
        bot.send(
            mode,
            user_id if mode == "private" else group_id,
            message=f"{id2name.get_name(user_id)}的灵魂不够了……",
        )
        return
    if gacha_res.startswith("NON"):
        bot.send(
            mode,
            user_id if mode == "private" else group_id,
            message=f"{id2name.get_name(user_id)}获得了{gacha_res}.\n请使用指令.non name 【名字】为其命名.",
        )
    bot.send(
        mode,
        user_id if mode == "private" else group_id,
        message=f"{id2name.get_name(user_id)}获得了{gacha_res}.",
    )


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
            non_species_name = get_non_entity(user_id, command_list[1]).species.name_cn
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
            message=f"已将暂存区的NON({non.species.name_cn})取名为{command_list[1]}.",
        )
        return

    elif not _check_temp_non(user_id):
        bot.send(
            mode,
            user_id if mode == "private" else group_id,
            message="暂存区中没有NON.",
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
            non_species_name = get_non_entity(user_id, command_list[2]).species.name_cn
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
            message=f"已将NON({command_list[1]})重命名为{command_list[2]}.",
        )
        return


def give_cmd(
    command_list: list[str],
    user_id: str,
    bot: OlivOS.API.Event,
    group_id: str = "",
):
    mode = "private" if group_id == "" else "group"
    if command_list[0].lower() != "give" or len(command_list) < 2:
        return
    if not _check_exist_non(user_id, command_list[1]):
        bot.send(
            mode,
            user_id if mode == "private" else group_id,
            message=f"没有名为{command_list[1]}的NON.",
        )
        return
    player = Player(user_id)
    non = get_non_entity(user_id, command_list[1])
    if non.in_battle != "":
        bot.send(
            mode,
            user_id if mode == "private" else group_id,
            message=f"{command_list[1]}正在进行战斗.",
        )
        return
    if len(command_list) == 2:
        if non.item is None:
            bot.send(
                mode,
                user_id if mode == "private" else group_id,
                message=f"{command_list[1]}身上没有物品.",
            )
            return
        player.set_item(non.item.name_cn, player.bag[non.item.name_cn] + 1)
        bot.send(
            mode,
            user_id if mode == "private" else group_id,
            message=f"已从{command_list[1]}身上拿下物品{non.item.name_cn}.",
        )
        non.item = None
        non.dump2json()

        return
    if player.bag[command_list[2]] < 1:
        bot.send(
            mode,
            user_id if mode == "private" else group_id,
            message="你没有这件东西.",
        )
        return
    # player.set_item(non.item.name, player.bag[non.item.name] - 1)
    temp_item = ""
    if non.item is not None:
        player.set_item(non.item.name_cn, player.bag[non.item.name_cn] - 1)
        temp_item = non.item.name_cn
    non.item = item_data_dict_cn[command_list[2]]
    non.dump2json()
    bot.send(
        mode,
        user_id if mode == "private" else group_id,
        message=(
            f"已给{non.name}携带{non.item.name_cn}."
            if temp_item == ""
            else f"已给{non.name}携带{non.item.name_cn}.({temp_item}已被放入背包)"
        ),
    )
    return


def team_cmd(
    command_list: list[str],
    user_id: str,
    bot: OlivOS.API.Event,
    group_id: str = "",
):
    mode = "private" if group_id == "" else "group"
    if command_list[0].lower() != "team":
        return
    player = Player(user_id)
    if len(command_list) == 1:
        team_str = ", ".join(player.team)
        bot.send(
            mode,
            user_id if mode == "private" else group_id,
            message=f"当前队伍为:\n{team_str}",
        )
        return
    team_list = command_list[1:]
    if len(team_list) > 4:
        bot.send(
            mode,
            user_id if mode == "private" else group_id,
            message="队伍长度最大为4.",
        )
        return
    invalid_name_list = []
    for non_name in team_list:
        if not _check_exist_non(user_id, non_name):
            invalid_name_list.append(non_name)
    if len(invalid_name_list) > 0:
        bot.send(
            mode,
            user_id if mode == "private" else group_id,
            message=f"你没有名为{','.join(invalid_name_list)}的NON.",
        )
        return
    player.team = team_list
    player.update_status()
    bot.send(
        mode,
        user_id if mode == "private" else group_id,
        message="成功更新队伍.",
    )
    return


def info_cmd(
    command_list: list[str],
    user_id: str,
    bot: OlivOS.API.Event,
    group_id: str = "",
):
    mode = "private" if group_id == "" else "group"
    if command_list[0].lower() != "info":
        return
    info_str = ""
    if len(command_list) == 1:
        app_json_path = "./plugin/app/NoName/app.json"
        if os.path.exists(app_json_path):
            with open(app_json_path, "r", encoding="utf-8") as f:
                version = json.load(f)["version"]
                info_str += f"NoName Game for You, Ver.{version}\nMade by: willkyu, mopo, 无敌火龙果"
        else:
            info_str += "NoName Game for You\nMade by: willkyu, mopo, 无敌火龙果"
    else:
        match command_list[1].lower():
            case "bag":
                player = Player(user_id)
                info_str += f"{player.nickname}的背包里有:\nCoin: {player.coin}\nDream Crystal: {player.dream_crystal}"
                for item_name, count in player.bag.items():
                    info_str += f"\n{item_name}: {count}"
            case "non":
                player = Player(user_id)
                if len(command_list) == 2:
                    non_list = []
                    for non_file_name in os.listdir(player.path + "NON/"):
                        if os.path.splitext(non_file_name)[1] == ".json":
                            non_list.append(os.path.splitext(non_file_name)[0])
                    for non_name in non_list:
                        non = get_non_entity(user_id, non_name)
                        info_str += f"· {non.name}({non.species.name_cn}) Lv.{non.level} gender:{non.gender}\n"
                elif not _check_exist_non(user_id, command_list[2]):
                    info_str += f"你没有名为{command_list[2]}的NON."
                else:
                    non = get_non_entity(user_id, command_list[2])
                    info_str += str(non)
            case "species":
                species_name = command_list[2]
                if len(command_list) < 3 or species_name not in species_data_dict_cn:
                    return
                info_str += str(species_data_dict_cn[species_name])
            case "item":
                item_name = command_list[2]
                if len(command_list) < 3 or item_name not in item_data_dict_cn:
                    return
                info_str += str(item_data_dict_cn[item_name])
            case "move":
                move_name = command_list[2]
                if len(command_list) < 3 or move_name not in move_data_dict_cn:
                    return
                info_str += str(move_data_dict_cn[move_name])
            case "ability":
                ability_name = command_list[2]
                if len(command_list) < 3 or ability_name not in ability_data_dict_cn:
                    return
                info_str += str(ability_data_dict_cn[ability_name])
            case "condition":
                condition_name = command_list[2]
                if (
                    len(command_list) < 3
                    or condition_name not in condition_data_dict_cn
                ):
                    return
                info_str += str(condition_data_dict_cn[condition_name])
            case _:
                info_str += "没有这条命令."

    bot.send(
        mode,
        user_id if mode == "private" else group_id,
        message=info_str,
    )


def use_cmd(
    command_list: list[str],
    user_id: str,
    bot: OlivOS.API.Event,
    group_id: str = "",
):
    mode = "private" if group_id == "" else "group"
    if command_list[0].lower() != "use" or len(command_list) < 2:
        return
    item_name = command_list[1]
    player = Player(user_id)
    if player.bag[item_name] < 1:
        bot.send(
            mode,
            user_id if mode == "private" else group_id,
            message="你没有这件东西.",
        )
        return
    # TODO 使用物品
    match item_name:
        case "童年的倒影":
            if _check_temp_non(user_id):
                species_name = get_non_entity(user_id).species.name_cn
                bot.send(
                    mode,
                    user_id if mode == "private" else group_id,
                    message=f"{id2name.get_name(user_id)}的暂存区中有未命名的NON({species_name})\n请先使用.non name 【NAME】对其命名.",
                )
                return
            if len(command_list) < 3 or command_list[2] not in area_data.keys():
                bot.send(
                    mode,
                    user_id if mode == "private" else group_id,
                    message=f"请输入AREA:\n{list(area_data.keys())}",
                )
                return
            gacha_res = gacha(player, command_list[2], mode="童年的倒影")
            if gacha_res.startswith("NON"):
                bot.send(
                    mode,
                    user_id if mode == "private" else group_id,
                    message=f"{id2name.get_name(user_id)}获得了{gacha_res}.\n倒影消散了.\n请使用指令.non name 【名字】为其命名.",
                )
                player.set_item(item_name, player.bag[item_name] - 1)
                return
            bot.send(
                mode,
                user_id if mode == "private" else group_id,
                message=f"{id2name.get_name(user_id)}获得了{gacha_res}.\n倒影还在那里.",
            )
            return
        case _:
            bot.send(
                mode,
                user_id if mode == "private" else group_id,
                message=f"{item_name}无法使用.",
            )
            return
    # player.set_item(item_name, player.bag[item_name] - 1)


def _check_exist_non(user_id: str, non_name: str):
    org_path = BASE_NON_FILE_PATH + f"{user_id}/NON/{non_name}.json"
    return os.path.exists(org_path)


def _check_temp_non(user_id: str):
    return os.path.exists(path=BASE_NON_FILE_PATH + f"{user_id}/TEMP.json")
