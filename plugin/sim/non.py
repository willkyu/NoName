from __future__ import annotations
from dataclasses import dataclass
from typing import Literal
from json import dump, load
import os

from .global_utils import (
    EVs,
    IVs,
    LevelRange,
    StatLevel,
    StatValue,
    Type,
    get_move_en,
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
from .data.ability_data import ability_data_dict_en
from .data.species_data import species_data_dict_en
from .data.item_data import item_data_dict_en


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
            self.move = get_move_en(self.name)
            self.id = self.move.id
            self.name_cn = self.move.name_cn
            self.pp = self.move.pp
            self.pp_max = self.pp


@dataclass
class NonTempBattleStatus:
    last_item: str = ""
    used_item_this_turn: bool = False


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
        if self.stat is None:
            self.calculate_stat()

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
                f"math.floor({10 if stat == 'HP' else 5}+(self.level*(2*self.species.species_strength.{stat}+self.ivs.{stat}+math.sqrt(self.evs.{stat}) / 8))/100)"
            )
        self.hp_max = stat_dict["HP"]
        self.hp = stat_dict["HP"]
        self.stat = StatValue(**{k: v for k, v in stat_dict.items() if k != "HP"})

    def save(self):
        self.dump2json()

    def dump2json(self, test=False):
        if not test:
            self.to_str()
        path = BASE_NON_FILE_PATH + "{}/NON/{}.json".format(self.master_id, self.name)
        if self.name == "":
            path = BASE_NON_FILE_PATH + "{}/TEMP.json".format(self.master_id)
        if test:
            path = "./"

        make_sure_dir(path)
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
        self.species = species_data_dict_en[self.species]
        self.ability = ability_data_dict_en[self.ability]
        self.item = item_data_dict_en[self.item] if self.item is not None else None
        if self.stat is not None:
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
        self.species = self.species.name
        self.ability = self.ability.name
        self.item = self.item.name if self.item is not None else None
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
        species=species.name,
        level=5,
        gender="N",
        in_battle="",
        ability="Hello World",
        move_slots={},
        ivs=IVs().__dict__,
        evs=EVs().__dict__,
    )


def init_move_slot(move_data: MoveData) -> MoveSlot:
    # TODO
    return MoveSlot(name="Tackle")
