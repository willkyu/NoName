from __future__ import annotations
from ..item import ItemData, rarity_list
from ..non_events import NonEvent, NonEventsObj
from .item_function import ItemFunctions

"""稀有度全部合并为在一起"""

item_data_base: list[ItemData] = [
    ItemData(
        id=1,
        name="Infinite Pitaya",
        name_cn="无限火龙果",
        rarity="PURPLE",
        desc="“这是什么？火龙果，吃一口. 这是什么？火龙果，吃一口.”\n给NON携带后，每次受到招式伤害恢复一定血量.",
        add_non_events=NonEventsObj(
            on_hit=[
                NonEvent(reason="无限火龙果", exe=ItemFunctions.infinite_pitaya_on_hit)
            ]
        ),
    ),
    ItemData(
        id=2,
        name="Reflection of MOPO",
        name_cn="童年的倒影",
        rarity="GOLD",
        desc="“看好了，我只演示一次.”\n进行一次无消耗gacha，如果结果不是NON则该物品不会消耗.",
        can_be_use=True,
    ),
    ItemData(
        id=3,
        name="Tiny Rice Dumpling",
        name_cn="小小的粽子",
        rarity="WHITE",
        desc="祝大家端午节快乐，之后将可以用于兑换其他物品.",
        can_be_use=True,
    ),
    ItemData(
        id=4,
        name="Huge Rice Dumpling",
        name_cn="巨大的粽子",
        rarity="Blue",
        desc="祝大家端午节快乐，之后将可以用于兑换其他物品.",
        can_be_use=True,
    ),
]

item_data_dict_en: dict[str, ItemData] = {
    item_data.name: item_data for item_data in item_data_base
}

item_data_dict_cn: dict[str, ItemData] = {
    item_data.name_cn: item_data for item_data in item_data_base
}

item_data_rarity: dict[str, ItemData] = {
    rarity: [
        item_data.name_cn for item_data in item_data_base if item_data.rarity == rarity
    ]
    for rarity in rarity_list
}
