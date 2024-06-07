import OlivOS
from .utils.config import *
from .utils.groupCommand import unityGroupReply
from .utils.privateCommand import unityPrivateReply
from .sim.battle import Battle

# activeGroupList = ["957736515"]
# masterList = ["496373158"]

config = Config()

botHash = "19e44f7870aaaa4d2cb384c92482ab79"
pluginName = "NoN"
botSend = None

parserPatterns: dict[str, dict[str, list[str]]] = {}
groupBattleDict: dict[str, Battle] = {}


def makeSureDir(path: str) -> None:
    if not os.path.exists(path):
        os.mkdir(path)


def initmsg(Proc):
    global botHash
    global botSend
    global pluginName
    botSend = OlivOS.API.Event(
        OlivOS.contentAPI.fake_sdk_event(
            bot_info=Proc.Proc_data["bot_info_dict"][botHash], fakename=pluginName
        ),
        Proc.log,
    )


class Event(object):
    def init(plugin_event, Proc):
        initmsg(Proc)
        pass

    def private_message(plugin_event, Proc):
        global botSend
        global groupBattleDict
        global parserPattern
        unityPrivateReply(
            plugin_event, config, botSend, parserPatterns, groupBattleDict
        )
        pass

    def group_message(plugin_event, Proc):
        global botSend
        global groupBattleDict
        global parserPattern
        unityGroupReply(plugin_event, config, botSend, parserPatterns, groupBattleDict)
        pass
