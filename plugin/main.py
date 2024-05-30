import OlivOS
from utils.config import Config
from utils.groupCommand import unity_group_reply


activeGroupList = ["957736515"]
masterList = ["496373158"]

config = Config(groupList=activeGroupList, masterList=masterList)

botHash = "19e44f7870aaaa4d2cb384c92482ab79"
pluginName = "NoN"
botSend = None


def initmsg(Proc):
    global botHash
    global botSend
    global pluginName
    botSend = OlivOS.API.Event(
        OlivOS.contentAPI.fake_sdk_event(
            bot_info=Proc.Proc_data["bot_info_dict"][botHash], fakename=pluginName
        ),
        Proc.log,
    ).send


class Event(object):
    def init(plugin_event, Proc):
        initmsg(Proc)
        pass

    def private_message(plugin_event, Proc):
        pass

    def group_message(plugin_event, Proc):
        global botSend
        unity_group_reply(plugin_event, Proc, config, botSend)
        pass
