from sim.battle import *

# from functools import partial


print("Done.")

# from sim.non import NON
# from plugin.sim.global_utils import *
# from sim.command import Command
# from time import sleep

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
battletest.add_player(mopo)

while not battletest.finished:
    command = input()
    exec(command)


battletest.add_command(mopo, "0")
battletest.add_command(mopo, "1")

battletest.add_command(willQ, "0")
battletest.add_command(willQ, "1")


battletest.add_command(mopo, "测试NON000", Command("测试NON", "move", "Tackle"))
battletest.add_command(mopo, "测试NON001", Command("测试NON003", "switch", ""))
battletest.add_command(willQ, "测试NON", Command("测试NON001", "move", "Tackle"))
battletest.add_command(willQ, "测试NON1", Command("测试NON001", "move", "Tackle"))

# battletest.addCommand(mopo, "测试NON000", Command("测试NON", "move", "Tackle"))
# battletest.addCommand(mopo, "测试NON003", Command("测试NON", "move", "Tackle"))
# battletest.addCommand(willQ, "测试NON", Command("测试NON003", "move", "Tackle"))
# battletest.addCommand(willQ, "测试NON1", Command("测试NON003", "move", "Tackle"))

# battletest.waitSwitchAdd(mopo, 1, "测试NON002")

# battletest.addCommand(mopo, "测试NON000", Command("测试NON", "move", "Tackle"))
# battletest.addCommand(mopo, "测试NON002", Command("测试NON", "move", "Tackle"))
# battletest.addCommand(willQ, "测试NON", Command("测试NON002", "move", "Tackle"))
# battletest.addCommand(willQ, "测试NON1", Command("测试NON002", "move", "Tackle"))

# battletest.waitSwitchAdd(willQ, 0, "测试NON2")

# battletest.addCommand(mopo, "测试NON000", Command("测试NON2", "move", "Tackle"))
# battletest.addCommand(mopo, "测试NON002", Command("测试NON1", "move", "Tackle"))
# battletest.addCommand(willQ, "测试NON2", Command("测试NON002", "move", "Tackle"))
# battletest.addCommand(willQ, "测试NON1", Command("测试NON002", "move", "Tackle"))

# battletest.waitSwitchAdd(mopo, 1, "测试NON001")

# battletest.addCommand(mopo, "测试NON000", Command("测试NON2", "move", "Tackle"))
# battletest.addCommand(mopo, "测试NON001", Command("测试NON1", "move", "Tackle"))
# battletest.addCommand(willQ, "测试NON2", Command("测试NON000", "move", "Tackle"))
# battletest.addCommand(willQ, "测试NON1", Command("测试NON000", "move", "Tackle"))

# battletest.addCommand(mopo, "测试NON000", Command("测试NON2", "move", "Tackle"))
# battletest.addCommand(mopo, "测试NON001", Command("测试NON1", "move", "Tackle"))
# battletest.addCommand(willQ, "测试NON2", Command("测试NON000", "move", "Tackle"))
# battletest.addCommand(willQ, "测试NON1", Command("测试NON000", "move", "Tackle"))

# battletest.waitSwitchAdd(willQ, 1, "测试NON3")

# battletest.addCommand(mopo, "测试NON000", Command("测试NON2", "move", "Tackle"))
# battletest.addCommand(mopo, "测试NON001", Command("测试NON1", "move", "Tackle"))
# battletest.addCommand(willQ, "测试NON3", Command("测试NON001", "move", "Tackle"))
# battletest.addCommand(willQ, "测试NON2", Command("测试NON001", "move", "Tackle"))

# battletest.addCommand(mopo, "测试NON000", Command("测试NON2", "move", "Tackle"))
# battletest.addCommand(mopo, "测试NON001", Command("测试NON1", "move", "Tackle"))
# battletest.addCommand(willQ, "测试NON3", Command("测试NON001", "move", "Tackle"))
# battletest.addCommand(willQ, "测试NON2", Command("测试NON001", "move", "Tackle"))
# battletest.
