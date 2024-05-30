import OlivOS
from utils.config import Config

activeGroupList = ["957736515"]
masterList = ["496373158"]

config = Config(groupList=activeGroupList, masterList=masterList)


class Event(object):
    def init(plugin_event, Proc):
        # repeater_init(plugin_event, Proc)
        pass

    def private_message(plugin_event, Proc):
        pass

    def group_message(plugin_event, Proc):
        # unity_reply(plugin_event, Proc)
        pass
