import OlivOS
import os

from .utils.config import Config
from .utils.group_cmd import unity_group_reply
from .utils.private_cmd import unity_private_reply
from .sim.battle import Battle
from .sim.global_utils import id2name

# activeGroupList = ["957736515"]
# masterList = ["496373158"]

config = Config()

BOT_HASH = "19e44f7870aaaa4d2cb384c92482ab79"
PLUGIN_NAME = "NoN"
bot_send = None

group_battle_dict: dict[str, Battle] = {}


def make_sure_dir(path: str) -> None:
    if not os.path.exists(path):
        os.mkdir(path)


def init_msg(Proc):
    global BOT_HASH
    global bot_send
    global PLUGIN_NAME
    bot_send = OlivOS.API.Event(
        OlivOS.contentAPI.fake_sdk_event(
            bot_info=Proc.Proc_data["bot_info_dict"][BOT_HASH], fakename=PLUGIN_NAME
        ),
        Proc.log,
    )

    global id2name
    id2name.update(
        {data["id"]: data["name"] for data in bot_send.get_friend_list()["data"]}
    )


class Event(object):
    def init(plugin_event, Proc):
        init_msg(Proc)
        pass

    def private_message(plugin_event, Proc):
        global bot_send
        global group_battle_dict
        unity_private_reply(plugin_event, config, bot_send, group_battle_dict)
        pass

    def group_message(plugin_event, Proc):
        global bot_send
        global group_battle_dict
        unity_group_reply(plugin_event, config, bot_send, group_battle_dict)
        pass
