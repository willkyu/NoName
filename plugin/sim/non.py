from __future__ import annotations
from dataclasses import dataclass
from typing import Literal
from json import dump, load
import os
import math  # noqa: F401
from copy import deepcopy

from .global_utils import (
    EVs,
    IVs,
    LevelRange,
    StatLevel,
    StatValue,
    Type,
    get_move_cn,
    make_sure_dir,
    stat_list,
    BASE_NON_FILE_PATH,
)
from .move import MoveData
from .species import SpeciesData
from .ability import Ability
from .item import ItemData
from .condition import Condition
from .non_events import NonEventsObj
from .data.ability_data import ability_data_dict_cn
from .data.species_data import species_data_dict_cn
from .data.item_data import item_data_dict_cn
from .data.condition_data import condition_data_dict_cn


@dataclass
class MoveSlot:
    name: str
    id: str = None
    name_cn: str = None
    move: MoveData = None
    pp: int = None
    pp_max: int = None
    used: bool = False
    target: str | None = None
    disabled: bool | str = False
    disabled_source: str | None = None

    def __post_init__(self):
        if self.name is not None:
            self.move = get_move_cn(self.name)
            self.id = self.move.id
            self.name_cn = self.move.name_cn
            self.pp = self.move.pp
            self.pp_max = self.pp


@dataclass
class NonTempBattleStatus:
    last_item: str = ""
    used_item_this_turn: bool = False
    protect: bool = False


@dataclass
class NON(object):
    name: str
    master_id: str
    species: SpeciesData | str
    level: LevelRange
    gender: Literal["M", "F", "N"]
    in_battle: str  # should be '' if not in battle
    ability: Ability | str

    move_slots: dict[str, MoveSlot]  # {moveNameEn, MoveSlot}
    ivs: IVs
    evs: EVs

    types: list[Type] = None
    conditions: dict[str, Condition] = None
    stat: StatValue = None
    hp: int = 0
    hp_max: int = 0
    battle_status: NonTempBattleStatus | None = None
    non_events: NonEventsObj = None
    item: ItemData | str = None
    stats_level: StatLevel = None

    def __post_init__(self):

        self.to_entity()
        self.calculate_stat()

    def add_condition(self, condition: str):
        self.conditions[condition] = deepcopy(condition_data_dict_cn[condition])
        for att in self.conditions[condition].add_non_events.__dict__.keys():
            exec(
                f"self.non_events.{att}+=self.conditions[condition].add_non_events.{att}"
            )

    def lose_conditions(self, reason: str):
        remove_dict = {}
        for att in self.non_events.__dict__.keys():
            remove_dict[att] = eval(f"self.non_events.{att}.remove{reason}")
        return remove_dict

    def hook_non_events(self):
        for att in self.ability.add_non_events.__dict__.keys():
            exec(f"self.non_events.{att}+=self.ability.add_non_events.{att}")
        if self.item is not None:
            for att in self.ability.add_non_events.__dict__.keys():
                exec(f"self.non_events.{att}+=self.item.add_non_events.{att}")

    def calculate_stat(self):
        stat_dict = {}
        for stat in stat_list:
            self.species.species_strength.HP
            self.ivs.HP
            self.evs.HP
            stat_dict[stat] = eval(
                f"math.floor({10+self.level if stat == 'HP' else 5}+(self.level*(2*self.species.species_strength.{stat}+self.ivs.{stat}+self.evs.{stat} / 4))/100)"
            )
        self.hp_max = stat_dict["HP"]
        self.hp = stat_dict["HP"]
        self.stat = StatValue(**{k: v for k, v in stat_dict.items() if k != "HP"})

    def save(self):
        self.dump2json()

    def dump2json(self, test=False):
        if not test:
            self.to_str()
        make_sure_dir(BASE_NON_FILE_PATH + f"{self.master_id}/NON/")
        path = BASE_NON_FILE_PATH + "{}/NON/{}.json".format(self.master_id, self.name)
        if self.name == "":
            path = BASE_NON_FILE_PATH + "{}/TEMP.json".format(self.master_id)
        if test:
            path = "./"

        # print(os.path.abspath(path))
        with open(path, "w+", encoding="utf-8") as f:
            dump(self, f, default=lambda obj: obj.__dict__, ensure_ascii=False)
        self.to_entity()

    def to_entity(self):
        self.stats_level = StatLevel()
        self.non_events = NonEventsObj()
        self.battle_status = NonTempBattleStatus()
        self.conditions = {}
        self.ivs = IVs(**self.ivs)
        self.evs = EVs(**self.evs)
        self.species = species_data_dict_cn[self.species]
        self.ability = ability_data_dict_cn[self.ability]
        self.item = item_data_dict_cn[self.item] if self.item is not None else None
        if self.stat is not None and isinstance(self.stat, dict):
            self.stat = StatValue(**self.stat)
        if self.types is None:
            self.types = self.species.types
        for k in self.move_slots.keys():
            self.move_slots[k] = MoveSlot(k)
        self.hook_non_events()

    def to_str(self):
        self.ivs = self.ivs.__dict__
        self.evs = self.evs.__dict__
        for k in self.move_slots.keys():
            self.move_slots[k] = {"name": k}
        self.stats_level = None
        self.species = self.species.name_cn
        self.ability = self.ability.name_cn
        self.item = self.item.name_cn if self.item is not None else None
        self.non_events = None
        self.battle_status = None
        self.conditions = None

    def load_from_json(self, master_id: str, non_name: str):
        # 可能用不上，直接在外部定义一个从json读类的就可以
        path = BASE_NON_FILE_PATH + "{}/NON/{}.json".format(master_id, non_name)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                self.__dict__.update(load(f))
            return True
        else:
            return False

    def __str__(self):
        non_str = ""
        non_str += f"{self.name}({self.species.name_cn}) Lv.{self.level} Gender: {self.gender}\n"
        non_str += f"Ability: {self.ability.name_cn} "
        non_str += "Item: {}\nMoves:\n".format(
            "no item" if self.item is None else self.item.name_cn
        )
        for moveslot in self.move_slots.values():
            move = moveslot.move
            non_str += f"{move.name_cn}({move.category}) Type:{move.type} pp: {moveslot.pp}/{moveslot.pp_max}\n"
            if move.base_power is not None:
                non_str += f"    Base Power: {move.base_power} "
            non_str += "    Accuracy: {}\n".format(
                "--" if isinstance(move.accuracy, bool) else move.accuracy
            )
        non_str += f"能力值:\nHP: {self.hp}/{self.hp_max}, ATK: {self.stat.ATK}, DEF: {self.stat.DEF}, SPA: {self.stat.SPA}, SPD: {self.stat.SPD}, SPE: {self.stat.SPE}"

        return non_str


def init_non_from_species(species: SpeciesData) -> NON:
    """调用完该方法请让玩家取名！默认名字为空字符串""
        此外masterId也需要绑定

    Args:
        species (SpeciesData): _description_

    Returns:
        NON: _description_
    """
    # TODO

    return NON(
        name="",
        master_id="",
        species=species.name_cn,
        level=5,
        gender="N",
        in_battle="",
        ability="你好世界",
        move_slots={},
        ivs=IVs().__dict__,
        evs=EVs().__dict__,
    )


def init_move_slot(move_data: MoveData) -> MoveSlot:
    # TODO
    return MoveSlot(name="撞击")
