from ..item import ItemData, Rarity

item_data_white: list[ItemData] = [
    ItemData(
        id=1,
        name="Tackle",
        name_cn="撞击",
        rarity=Rarity.WHITE,
        category="Physical",
        type="Normal",
        target="normal",
        base_power=40,
        accuracy=100,
        desc="使用全身的力气撞击目标。",
    ),
    ItemData(
        id=2,
        name="Ember",
        name_cn="火花",
        pp=30,
        category="Magical",
        type="Fire",
        target="normal",
        base_power=40,
        accuracy=100,
        desc="向目标发射小小的火苗。有时会令目标烧伤。",
        # 怎么导致异常状态呢？函数还是变量
    ),
]

item_data_blue: list[ItemData] = [
    ItemData(
        id=1,
        name="Tackle",
        name_cn="撞击",
        rarity=Rarity.BLUE,
        category="Physical",
        type="Normal",
        target="normal",
        base_power=40,
        accuracy=100,
        desc="使用全身的力气撞击目标。",
    )
]

item_data_purple: list[ItemData] = [
    ItemData(
        id=1,
        name="Tackle",
        name_cn="撞击",
        rarity=Rarity.PURPLE,
        category="Physical",
        type="Normal",
        target="normal",
        base_power=40,
        accuracy=100,
        desc="使用全身的力气撞击目标。",
    )
]

item_data_gold: list[ItemData] = [
    ItemData(
        id=1,
        name="Tackle",
        name_cn="撞击",
        rarity=Rarity.GOLD,
        category="Physical",
        type="Normal",
        target="normal",
        base_power=40,
        accuracy=100,
        desc="使用全身的力气撞击目标。",
    )
]

itemData = item_data_white + item_data_blue + item_data_purple + item_data_gold

itemDataDictEn: dict[str, ItemData] = {itemData.name: itemData for itemData in itemData}

itemDataDictCn: dict[str, ItemData] = {
    itemData.name_cn: itemData for itemData in itemData
}
