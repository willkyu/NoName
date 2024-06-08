from __future__ import annotations
from ..item import ItemData, Rarity
from ..non_events import NonEvent, NonEventsObj
from .item_function import ItemFunctions

"""稀有度全部合并为在一起"""

item_data_base: list[ItemData] = [
    ItemData(
        id=1,
        name="Infinite Pitaya",
        name_cn="无限火龙果",
        rarity=Rarity.WHITE,
        desc="这是什么？火龙果，吃一口。这是什么？火龙果，吃一口。",
        add_non_events=NonEventsObj(
            on_hit=[
                NonEvent(reason="无限火龙果", exe=ItemFunctions.infinite_pitaya_on_hit)
            ]
        ),
    ),
]

item_data_dict_en: dict[str, ItemData] = {
    item_data.name: item_data for item_data in item_data_base
}

item_data_dict_cn: dict[str, ItemData] = {
    item_data.name_cn: item_data for item_data in item_data_base
}
