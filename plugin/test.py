from sim.battle import *


print("Done.")


commandPriorityDict = {"a": 3, "b": 2, "c": 3, "d": 1}
# print(
#     [
#         key
#         for key, value in sorted(
#             commandPriorityDict.items(), key=lambda x: (-x[1][0], -x[1][1])
#         )
#     ]
# )

print(
    [
        key
        for key in sorted(
            commandPriorityDict.keys(), key=lambda x: (-commandPriorityDict[x])
        )
    ]
)

# test = getNickname("403363659")
# print(test)
