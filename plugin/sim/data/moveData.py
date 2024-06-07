from ..move import MoveData

moveDataBase: list[MoveData] = [
    MoveData(
        id=1,
        name="Tackle",
        nameCn="撞击",
        pp=40,
        category="Physical",
        type="Normal",
        target="normal",
        basePower=40,
        accuracy=100,
        desc="使用全身的力气撞击目标。",
    ),
    MoveData(
        id=2,
        name="Ember",
        nameCn="火花",
        pp=30,
        category="Magical",
        type="Fire",
        target="normal",
        basePower=40,
        accuracy=100,
        desc="向目标发射小小的火苗。有时会令目标烧伤。",
        # 怎么导致异常状态呢？函数还是变量
    ),
]

moveDataDictEn: dict[str, MoveData] = {
    moveData.name: moveData for moveData in moveDataBase
}

moveDataDictCn: dict[str, MoveData] = {
    moveData.nameCn: moveData for moveData in moveDataBase
}
