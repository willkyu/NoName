from sim.globalUtils import *


class Player:
    id: str
    path: str
    team: Annotated[list[str], "len must <= 6"] | None
    coin: int = 0
    dreamCrystal: int

    def __init__(self, playerId: str) -> None:
        self.id = playerId
        self.path = baseNonFilePath + "{}/".format(self.id)
        if not os.path.exists(self.path + "userConfig.json"):
            createNewConfig(self.id)
        with open(self.path + "userConfig.json") as f:
            self.__dict__.update()
        self.coin = readCoin(self.id)
        pass

    def __str__(self) -> str:
        return "————————————\n▼ ID[{}]身份认证成功.\n┣———————————\n│ 灵魂：{}\n│ DreamCrystal：{}\n————————————".format(
            self.id, self.coin, self.dreamCrystal
        )
