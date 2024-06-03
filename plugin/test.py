from sim.battle import *


print("Done.")


commandPriorityDict = {"a": (3, 5), "b": (2, 7), "c": (3, 2), "d": (1, 6)}
print(
    [
        key
        for key, value in sorted(
            commandPriorityDict.items(), key=lambda x: (-x[1][0], -x[1][1])
        )
    ]
)


test = getNickname("403363659")
print(test)
