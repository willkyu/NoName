import json
import os
from typing import Literal

BASE_DATA_FILE_PATH = "./plugin/data/NoName/"


class Config:
    active_group_list: list[str]
    master_list: list[str]

    def __init__(self) -> None:
        # global baseDataFilePath
        if not os.path.exists(BASE_DATA_FILE_PATH + "config.json"):
            self.init_config_file()
        with open(BASE_DATA_FILE_PATH + "config.json", "r", encoding="utf-8") as f:
            self.__dict__.update(json.load(f))
            print(self.__dict__)

    def init_config_file(self):
        self.active_group_list = ["957736515"]
        self.master_list = ["496373158"]
        self.write_config()

    def write_config(self):
        with open(BASE_DATA_FILE_PATH + "config.json", "w+", encoding="utf-8") as f:
            json.dump(self, f, default=lambda obj: obj.__dict__, ensure_ascii=False)

    def edit_config(
        self, id: str, mode: Literal["group", "master"], add_mode: bool = True
    ):
        if add_mode:
            if mode == "group" and id not in self.active_group_list:
                self.active_group_list.append(id)
            elif mode == "master" and id not in self.master_list:
                self.master_list.append(id)
            else:
                return
        else:
            if mode == "group" and id in self.active_group_list:
                self.active_group_list.remove[id]
            elif mode == "master" and id in self.master_list:
                self.master_list.remove[id]
            else:
                return
        self.write_config()
