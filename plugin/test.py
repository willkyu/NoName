from sim.battle import *

# from functools import partial


print("Done.")


commandPriorityDict = {"a": 3, "b": 2, "c": 3, "d": 1}

from sim.non import NON
from sim.globalUtils import *
from sim.command import Command
from time import sleep

# nontest = NON(
#     name="测试NON",
#     masterId="496373158",
#     species="NillKyu",
#     level=5,
#     gender="N",
#     inBattle="",
#     ability="Hello World",
#     moveSlots={"Tackle": {"name": "Tackle"}},
#     ivs=IVs().__dict__,
#     evs=EVs().__dict__,
# )
# nontest.dump2Json()

# nontest = getNonEntity("496373158", "测试NON")
# print(nontest)
# nontest.hp = nontest.hpmax
# nontest.dump2Json()


class botTest:
    def send(self, x, y, z):
        print("Get Bot Send ({},{}):\n{}".format(x, y, z))


mopo = "403363659"
willQ = "496373158"

battletest = Battle(willQ, "131313", "double", botTest())
battletest.addPlayer(mopo)

battletest.addCommand(mopo, 0, Command("测试NON", "move", "Tackle"))
# print("mopo send command0")
# sleep(1)


battletest.addCommand(mopo, 1, Command("测试NON1", "move", "Tackle"))
# print("mopo send command1")
# sleep(1)

battletest.addCommand(willQ, 0, Command("测试NON000", "move", "Tackle"))
# print("willq send command0")
# sleep(1)

battletest.addCommand(willQ, 1, Command("测试NON000", "move", "Tackle"))
# print("willq send command1")
# sleep(1)
# battletest.
