from sim.item import ItemData, Rarity

itemDataWhite: list[ItemData] = [
    ItemData(
        id=1,
        name="Tackle",
        nameCn="撞击",
        rarity=Rarity.WHITE,
        category="Physical",
        type="Normal",
        target="normal",
        basePower=40,
        accuracy=100,
        desc="使用全身的力气撞击目标。",
    ),
    ItemData(
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

itemDataBlue: list[ItemData] = [
    ItemData(
        id=1,
        name="Tackle",
        nameCn="撞击",
        rarity=Rarity.BLUE,
        category="Physical",
        type="Normal",
        target="normal",
        basePower=40,
        accuracy=100,
        desc="使用全身的力气撞击目标。",
    )
]

itemDataPurple: list[ItemData] = [
    ItemData(
        id=1,
        name="Tackle",
        nameCn="撞击",
        rarity=Rarity.PURPLE,
        category="Physical",
        type="Normal",
        target="normal",
        basePower=40,
        accuracy=100,
        desc="使用全身的力气撞击目标。",
    )
]

itemDataGold: list[ItemData] = [
    ItemData(
        id=1,
        name="Tackle",
        nameCn="撞击",
        rarity=Rarity.GOLD,
        category="Physical",
        type="Normal",
        target="normal",
        basePower=40,
        accuracy=100,
        desc="使用全身的力气撞击目标。",
    )
]

itemData = itemDataWhite + itemDataBlue + itemDataPurple + itemDataGold

itemDataDictEn: dict[str, ItemData] = {
    itemData.name: itemData for itemData in itemData
}

itemDataDictCn: dict[str, ItemData] = {
    itemData.nameCn: itemData for itemData in itemData
}
