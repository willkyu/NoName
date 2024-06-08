import OlivOS
from ..sim.global_utils import battle_mode, battle_mode_dsc
from ..sim.roll import ITEAMRATE


def help_cmd(
    command_list: list[str],
    user_id: str,
    bot: OlivOS.API.Event,
    group_id: str = "",
):

    if command_list[0] != "help":
        return

    mode = "private" if group_id == "" else "group"

    helpmsg = ""

    if len(command_list) == 1:
        helpmsg += ".non 后接指令:\n"
        helpmsg += "[开始战斗] 群聊限定. 开启或参与一场对战.\n"
        helpmsg += "[gacha] 进行一次抽奖.\n"
        helpmsg += "[name] 对NON进行命名/重命名.\n"
        helpmsg += "[info] 查看指定内容的详情（暂未实现）."
    elif command_list[1] == "开始战斗":
        helpmsg += ".non 开始战斗:\n"
        helpmsg += "群聊限定. \n"
        helpmsg += "如果当前群聊已有一场他人发起的战斗就会自动参与.\n"
        helpmsg += (
            "如果当前群聊没有他人发起的战斗，你需要在后面额外加一个参数BattleMode.\n"
        )
        helpmsg += f"BattleMode的可选值有: {battle_mode}.\n"
        helpmsg += f"它们的含义分别为: {battle_mode_dsc}."
    elif command_list[1] == "gacha":
        helpmsg += ".non gacha:\n"
        helpmsg += "进行一次抽奖.\n"
        helpmsg += f"当前概率为物品{ITEAMRATE*100:.2f}%，NON{100-ITEAMRATE*100:.2f}%.\n"
        helpmsg += "· 如果抽到NON会存入你的暂存区.\n"
        helpmsg += "  暂存区需要使用.non name命令进行命名才会算入你拥有的NON.\n"
        helpmsg += "  一个人只有一个暂存区，如果暂存区中有未命名的NON，你将无法gacha.\n"
        helpmsg += "· 如果抽到物品会存入你的背包.\n"
        helpmsg += "  你可以使用.non info bag指令查看你的背包."
    elif command_list[1] == "name":
        helpmsg += ".non name:\n"
        helpmsg += "这个指令后必须接其他参数.\n"
        helpmsg += "以下指令例子中的中括号都是不需要的.\n"
        helpmsg += "对你的NON进行命名/重命名.\n"
        helpmsg += "· .non name [NonName]:\n"
        helpmsg += "  为暂存区中的NON取名.\n"
        helpmsg += "· .non name [NonName1] [NonName2]:\n"
        helpmsg += "  将你的名为NonName1的NON重命名为NonName2.\n"
        helpmsg += "**注意，起名请勿带标点符号或其他特殊字符，只建议中英文**"
    elif command_list[1] == "info":
        helpmsg += ".non info:\n"
        helpmsg += "以下指令例子中的中括号都是不需要的.\n"
        helpmsg += "查看指定内容的详情.\n"
        helpmsg += "· .non info bag:\n"
        helpmsg += "  查看你的背包.\n"
        helpmsg += "· .non info non [NonName]:\n"
        helpmsg += "  查看你的NON信息，如果在对战中会显示对战状态\n"
        helpmsg += "· .non info ability [AbilityName]:\n"
        helpmsg += "  查看名为AbilityName的特性名称\n"
        helpmsg += "· .non info item [ItemName]:\n"
        helpmsg += "  查看名为ItemName的物品名称\n"

    bot.send(
        mode,
        user_id if mode == "private" else group_id,
        message=helpmsg,
    )
