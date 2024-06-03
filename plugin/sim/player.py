import random

from sim.globalUtils import *
from sim.livingArea import Area


class Player:
    id: str
    nickname: str
    path: str
    team: Annotated[list[str], "len must <= 6"] | None
    coin: int = 0
    dreamCrystal: int

    def __init__(self, playerId: str) -> None:
        self.id = playerId
        self.nickname = getNickname(self.id)
        self.path = baseNonFilePath + "{}/".format(self.id)
        if not os.path.exists(self.path + "userConfig.json"):
            createNewConfig(self.id)
        with open(self.path + "userConfig.json") as f:
            self.__dict__.update()
        self.coin = readCoin(self.id)
        pass

    def __str__(self) -> str:
        return "————————————\n▼ ID[{}]身份认证成功.\n▼ 以[{}]进行登入.\n┣———————————\n│ 灵魂：{}\n│ DreamCrystal：{}\n————————————".format(
            self.id, self.coin, self.dreamCrystal
        )

    # 玩家获取新的NonBaby
    def findNonBaby(self, msg: str):
        """
        TODO 这里我觉得应该直接传入参数了，比如区域的str，
             指令直接在外部处理指令的地方判断。
        """
        global nonBabyId
        if self.coin < 10:
            return "余额为:{" + str(self.coin) + "},余额不足请下次再来捏"
        elif msg == ".获取NonBaby":
            nonBabyId = self.getRandomNonBabyId()
            self.coin += -10
            return nonBabyId
        elif msg == ".获取沙漠NonBaby":
            if self.coin < 20:
                return "余额为:{" + str(self.coin) + "},余额不足请下次再来捏"
            nonBabyId = self.getRandomNonBabyId()
            self.coin += -20
            return

    def getRandomNonBabyId(self):
        # 占位 做动态出现率
        return random.randint(1, 10000)

    def judgeCoin(self, district: str):
        # 阶段收费
        if district == "":
            return self.coin > 10
        elif district == Area.DESERT:
            return self.coin > 20
