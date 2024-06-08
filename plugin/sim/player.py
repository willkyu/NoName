import os
import random
import json
from typing import Annotated
from collections import defaultdict

from .global_utils import (
    create_new_config,
    get_nickname,
    make_sure_dir,
    BASE_NON_FILE_PATH,
    read_coin,
)


class Player:
    id: str
    nickname: str
    path: str
    team: Annotated[list[str], "len must <= 6"] | None
    dream_crystal: int = 0
    coin: int = 0
    bag: dict[str:int] = None

    def __init__(self, player_id: str) -> None:
        self.id = player_id
        self.bag = None
        # print("getting name")
        self.nickname = get_nickname(self.id)
        # print(self.nickname)
        self.path = BASE_NON_FILE_PATH + "{}/".format(self.id)
        make_sure_dir(self.path)
        if not os.path.exists(self.path + "userConfig.json"):
            create_new_config(self.id)
        with open(self.path + "userConfig.json", "r", encoding="utf-8") as f:
            self.__dict__.update(json.load(f))
        self.coin = read_coin(self.id)
        # print(self.__dict__)

        if self.bag is None:
            self.bag = {}
        self.bag = defaultdict(int, self.bag)
        pass

    def __str__(self) -> str:
        return "————————————\n▼ ID[{}]身份认证成功.\n▼ 以[{}]进行登入.\n┣———————————\n│ 灵魂：{}\n│ DreamCrystal：{}\n————————————".format(
            self.id, self.nickname, self.coin, self.dream_crystal
        )

    # 玩家获取新的NonBaby
    def get_non(self, msg: str):
        """
        TODO 这里我觉得应该直接传入参数了，比如区域的str，
             指令直接在外部处理指令的地方判断。
        """
        # global nonBabyId
        if self.coin < 10:
            return "余额为:{" + str(self.coin) + "},余额不足请下次再来捏"
        elif msg == ".获取NonBaby":
            non_baby_id = self.get_random_non_id()
            self.coin += -10
            return non_baby_id
        elif msg == ".获取沙漠NonBaby":
            if self.coin < 20:
                return "余额为:[" + str(self.coin) + "],余额不足请下次再来捏"
            non_baby_id = self.get_random_non_id()
            self.coin += -20
            return

    def get_random_non_id(self, area: str):
        # 占位 做动态出现率
        return random.randint(1, 10000)

    def judge_coin(self, district: str):
        # 阶段收费
        if district == "":
            return self.coin > 10
        elif district == "沙漠":
            return self.coin > 20

    def update_status(self):
        self.bag = dict(**self.bag)
        # 将JSON数据写入文件
        with open(self.path + "userConfig.json", "w+", encoding="utf-8") as file:
            json.dump(self, file, indent=4, ensure_ascii=False)
        self.bag = defaultdict(int, self.bag)

    def set_item(self, item: str, count):
        self.bag[item] = count
        self.update_status()
