from utils.battleClass import BattleStage
import pickle


class Move(object):
    def __init__(self) -> None:
        self.moveType = "normal"
        self.type = "special"
        # self
        pass

    def calculateDamage(self, battleStage: BattleStage, org, tar):
        pass

    def exe(self, battleStage: BattleStage, botSend: function, target, origin):
        pass


class mytestmove(Move):
    def __init__(self) -> None:
        super().__init__()

    def exe(self, battleStage: BattleStage, botSend: function, target, origin):
        # do your move here
        pass
        return super().exe(battleStage, botSend, target, origin)


savePath = "your savepath"
moveInstance = mytestmove()
with open(savePath, "rb") as f:
    pickle.dump(savePath, f)
