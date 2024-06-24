# Contribute to NoName Dataset

这篇readme用于解释如何向data文件夹中添加你的构思（如NON种类、招式、特性、道具、状态等等）。

## 种类 Species

`species_data.py`

我们以甜粽子为例：

```python
SpeciesData(
    name="Sweericepling",
    name_cn="甜粽子",
    index=1,
    base_rate_buff=5,
    types=["Normal", "Water"],
    abilities=SpeciesAbilities(
        A1=ability_data_dict_cn["你好世界"],
        A2=ability_data_dict_cn["踩踩水花"],
        H=ability_data_dict_cn["死者苏生"],
    ),
    rate_buff=normal_rate_buff,
    species_strength=SpeciesStrength(HP=65, ATK=30, DEF=40, SPA=50, SPD=40, SPE=60),
    move_learn_set={
        1: "撞击",
        6: "保护",
        14: "祈雨",
        20: "闪击",
        26: "一拳",
        32: "原子尘埃",
    },
    desc="端午节快乐~大家该吃甜粽子啦.",
),
```

|attribute|explanation|
| :----: | :---- |
|name|英文名|
|name_cn|中文名|
|index|序号，按顺序往下就行|
|base_rate_buff|基础抽中的概率|
|types|属性，暂时还没定有哪些|
|abilities|特性，其中A1，A2是正常能抽出来的，H是隐藏特性，一般是活动解锁此外一个NON实体只会有一个特性，从中抽选|
|rate_buff|特殊的抽中概率调整值，见下，如果懒得管就直接用normal_rate_buff|
|species_strength|种族值，这个种族的六维，分别是血量HP，物理攻击ATK，物理防御DEF，魔法攻击SPA，魔法防御SPD，速度SPE|
|move_learn_set|字典，在几级学习什么技能当第一次获得时会从中roll四个直接学会|
|desc|描述，多写写|


- rate_buff

    ```python
    spring_rate_buff: int,
    summer_rate_buff: int,
    autumn_rate_buff: int,
    winter_rate_buff: int,
    morning_rate_buff: int,
    noon_rate_buff: int,
    afternoon_rate_buff: int,
    night_rate_buff: int
    ```

## 招式 Move

`move_data.py`

以火花为例：

```python
MoveData(
    id=2,
    name="Ember",
    name_cn="火花",
    pp=35,
    category="Magical",
    type="Fire",
    target="normal",
    base_power=40,
    accuracy=100,
    desc="向目标发射小小的火苗。有时会令目标烧伤.",
    secondary=partial(MoveFunctions.may_burnt, chance=0.25),
),
```

|attribute|explanation|
| :----: | :---- |
|id|序号，就是index|
|name|英文名|
|name_cn|中文名|
|pp|使用次数|
|category|类型，"Physical"、"Magical"、"Auxiliary"分别代表物理攻击、魔法攻击和辅助招式|
|type|招式的属性，同Species里的type|
|target|招式的可选目标，一般是"normal"可选除了自己外任意一个。所有的target见下|
|base_power|基础伤害，如果category是"Auxiliary"就不需要这个attribute|
|accuracy|基础命中率，暂时还没写命中相关的代码|
|desc|描述，可以多写一点|
|secondary|招式命中后触发的效果，具体写在`move_function.py`中|
|condition|招式使用前触发的效果，具体写在`move_function.py`中|
|priority|先制度，默认为0，越高越快|

- target

    ```python
        target: Literal[
                "adjacentAlly",  # 相邻队友
                "adjacentAllyOrSelf",  # 相邻队友或自身
                "adjacentFoe",  # 相邻敌方
                "all",  # 所有或是影响field
                "allAdjacent",  # 相邻所有
                "allAdjacentFoes",  # 相邻所有敌方
                "allies",  # 所有在场队友
                "allySide",  # 队友侧
                "allyTeam",  # 队友（包括不在场队友，不包括fainted的）
                "any",  # 任意一个
                "foeSide",  # 敌方侧
                "normal",  # 任意一个相邻
                "randomNormal",  # 随机一个相邻
                "scripted",  # 反伤
                "self",  # 自己
            ]
    ```

### 招式效果 move_function

`move_function.py`

依葫芦画瓢写就行，然后绑定到招式的condition或者secondary里。
其中field里可用的函数会在下面提到。

## 特性 Ability

`ability_data.py`

以你好世界为例：

```python
Ability(
    id=1,
    name="Hello World",
    name_cn="你好世界",
    desc="“print('Hello World')”\n出场时所有队友攻击等级+1.",
    add_non_events=NonEventsObj(
        on_active_once=[
            NonEvent(reason="你好世界", exe=AbilityFunctions.hello_world)
        ]
    ),
),
```

|attribute|explanation|
| :----: | :---- |
|id|序号，就是index|
|name|英文名|
|name_cn|中文名|
|desc|描述，尽情发挥你的想象力|
|add_non_events|特性效果函数，NonEventsObj中对应的attribute就决定了后面绑定的NonEvent在什么时候触发，比如on_active_once就是出场触发一次，on_hit就是被攻击招式命中后触发一次，具体有哪些见下|

- NonEventsObj

    ```python
    on_active_once: NonEventList = None # 出场触发一次
    before_switch: NonEventList = None  # 交换前触发
    after_switch: NonEventList = None   # 交换后触发
    on_weather_changed: NonEventList = None # 天气变化时触发
    end_of_turn: NonEventList = None    # 每回合结束触发
    start_of_turn: NonEventList = None  # 每回合开始触发
    on_get: NonEventList = None # 这是什么，我不记得了
    on_hit: NonEventList = None # 被攻击招式命中后触发
    ```

## 道具 Item

`item_data.py`

以无限火龙果和童年的倒影为例：

```python
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
```

|attribute|explanation|
| :----: | :---- |
|id|序号，就是index|
|name|英文名|
|name_cn|中文名|
|rarity|稀有度，决定了抽取的难度|
|desc|描述，可以写得玄乎一点|
|consumable|默认False，是否是战斗中的消耗品|
|can_be_use|是否战斗外可以直接使用|
|add_non_events|同特性，当这个物品被装备到NON身上时会带来的被动，写在`item_function.py`里|



## 特性效果、道具效果 ability_function、item_function

`ability_function.py`、`item_function.py`

照葫芦画瓢即可，一般来说kwargs['org']是该事件的拥有者的tuple（tuple你可以理解为用于定位的一对参数，第一个是str代表userid，第二个是int代表第几只NON）。

## 状态 Condition

看了特性和道具应该不用我多介绍了，效果函数在`condition_function.py`里

## Field的一些接口

- make_damage 造成伤害一定要用这个写，不然会有bug
- get_non_tuple 给定一个non的名字，获取他的tuple。tuple可以理解为是该non的定位符
- update_weather 改变天气
- get_ally_non 获取给定的non的队友的列表（在场上），alive默认为True，也就是说默认获取活着的队友的列表
- get_all_non 获取场上所有或者的non列表
- revive_non 复活non
- recover 给non恢复血量

具体的输入输出在field.py里有注释，可以去看一下



