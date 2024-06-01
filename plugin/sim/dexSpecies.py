from typing import Literal

from sim.dexData import BasicEffect, toID


class Species(BasicEffect):
    """ """

    """
    Species ID. Identical to ID. Note that this is the full ID, e.g.
    'basculinbluestriped'. To get the base species ID, you need to
    manually read toID(species.baseSpecies).
    """
    id: str
    """
    Name. Note that this is the full name with forme,
    e.g. 'Basculin-Blue-Striped'. To get the name without forme, see
    `species.baseSpecies`.
    """
    name: str
    """
    Base species. Species, but without the forme name.

    DO NOT ASSUME A POKEMON CAN TRANSFORM FROM `baseSpecies` TO
    `species`. USE `changesFrom` FOR THAT.
    """
    baseSpecies: str
    """
    Forme name. If the forme exists,
    `species.name === species.baseSpecies + '-' + species.forme`

    The games make a distinction between Forme (foorumu) (legendary Pokémon)
    and Form (sugata) (non-legendary Pokémon). PS does not use the same
    distinction – they're all "Forme" to PS, reflecting current community
    use of the term.

    This property only tracks non-cosmetic formes, and will be `''` for
    cosmetic formes.
    """
    forme: str
    """
    Base forme name (e.g. 'Altered' for Giratina).
    """
    baseForme: str
    """
    Other forms. List of names of cosmetic forms. These should have
    `aliases.js` aliases to this entry, but not have their own
    entry in `pokedex.js`.
    """
    cosmeticFormes: list[str] | None
    """
    Other formes. List of names of formes, appears only on the base
    forme. Unlike forms, these have their own entry in `pokedex.js`.
    """
    otherFormes: list[str] | None
    """
    List of forme speciesNames in the order they appear in the game data -
    the union of baseSpecies, otherFormes and cosmeticFormes. Appears only on
    the base species forme.

    A species's alternate formeindex may change from generation to generation -
    the forme with index N in Gen A is not guaranteed to be the same forme as the
    forme with index in Gen B.

    Gigantamaxes are not considered formes by the game (see data/FORMES.md - PS
    labels them as such for convenience) - Gigantamax "formes" are instead included at
    the end of the formeOrder list so as not to interfere with the correct index numbers.
    """
    formeOrder: list[str] | None
    """
    Sprite ID. Basically the same as ID, but with a dash between
    species and forme.
    """
    spriteid: str
    """
    Abilities.
    """
    abilities: dict[str, list[str]]
    """
    Types.
    """
    types: list[str]
    """
    Added type (added by Trick-Or-Treat or Forest's Curse, but only listed in species by OMs).
    """
    addedType: str | None
    """
    Pre-evolution. '' if nothing evolves into this Pokemon.
    """
    prevo: str
    """
    Evolutions. Array because many Pokemon have multiple evolutions.
    """
    evos: list[str]
    evoType: str | None
    """
    Evolution condition. falsy if doesn't evolve.
    """
    evoCondition: str | None
    """
    Evolution item. falsy if doesn't evolve.
    """
    evoItem: str | None
    """
    Evolution move. falsy if doesn't evolve.
    """
    evoMove: str | None
    """
    Region required to be in for evolution. falsy if doesn't evolve.
    """
    evoRegion: str | None
    """
    Evolution level. falsy if doesn't evolve.
    """
    evoLevel: int | None
    """
    Is NFE? True if this Pokemon can evolve (Mega evolution doesn't count).
    """
    nfe: bool
    """
    Egg groups.
    """
    eggGroups: list[str]
    """
    True if this species can hatch from an Egg.
    """
    canHatch: bool
    """
    Gender. M = always male, F = always female, N = always
    genderless, '' = sometimes male sometimes female.
    """
    gender: str
    """
    Gender ratio. Should add up to 1 unless genderless.
    """
    genderRatio: dict[str, float]
    """
    Base stats.
    """
    baseStats: dict[str, int]
    """
    Max HP. Overrides usual HP calculations (for Shedinja).
    """
    maxHP: int | None
    """
    A Pokemon's Base Stat Total
    """
    bst: int
    """
    Weight (in kg). Not valid for OMs; use weighthg / 10 instead.
    """
    weightkg: float
    """
    Weight (in integer multiples of 0.1kg).
    """
    weighthg: int
    """
    Height (in m).
    """
    heightm: float
    """
    Color.
    """
    color: str
    """
    Tags, boolean data. Currently just legendary/mythical status.
    """
    tags: list[str]
    """
    Does this Pokemon have an unreleased hidden ability?
    """
    unreleasedHidden: bool | str
    """
    Is it only possible to get the hidden ability on a male pokemon?
    This is mainly relevant to Gen 5.
    """
    maleOnlyHidden: bool
    """
    True if a pokemon is mega.
    """
    isMega: bool | None
    """
    True if a pokemon is primal.
    """
    isPrimal: bool | None
    # """
    # Name of its Gigantamax move, if a pokemon is capable of gigantamaxing.
    # """
    # canGigantamax: str | None
    # """
    # If this Pokemon can gigantamax, is its gigantamax released?
    # """
    # gmaxUnreleased: bool | None
    # """
    # True if a Pokemon species is incapable of dynamaxing
    # """
    # cannotDynamax: bool | None
    # """
    # The Tera Type this Pokemon is forced to use
    # """
    # forceTeraType: str | None
    """
    What it transforms from, if a pokemon is a forme that is only accessible in battle.
    """
    battleOnly: str | list[str] | None
    """
    Required item. Do not use this directly; see requiredItems.
    """
    requiredItem: str | None
    """
    Required move. Move required to use this forme in-battle.
    """
    requiredMove: str | None
    """
    Required ability. Ability required to use this forme in-battle.
    """
    requiredAbility: str | None
    """
    Required items. Items required to be in this forme, e.g. a mega
    stone, or Griseous Orb. Array because Arceus formes can hold
    either a Plate or a Z-Crystal.
    """
    requiredItems: list[str] | None
    """
    Formes that can transform into this Pokemon, to inherit learnsets
    from. (Like `prevo`, but for transformations that aren't
    technically evolution. Includes in-battle transformations like
    Zen Mode and out-of-battle transformations like Rotom.)

    Not filled out for megas/primals - fall back to baseSpecies
    for in-battle formes.
    """
    changesFrom: str | None

    def __init__(self, data: object) -> None:
        super().__init__(data)
        data = self

        self.fullname = "NON: ".format(self.naem)
        self.effectType = "NON"
        self.baseSpecies = data.baseSpecies or self.name
        self.forme = data.forme or ""
        self.baseForme = data.baseForme or ""
        self.cosmeticFormes = data.cosmeticFormes or None
        self.otherFormes = data.otherFormes or None
        self.formeOrder = data.formeOrder or None
        self.spriteid = data.spriteid or (
            toID(self.baseSpecies)
            + ("-" + toID(self.forme) if self.baseSpecies != self.name else "")
        )
        self.abilities = data.abilities or {0: ""}
        self.types = data.types or ["???"]
        self.addedType = data.addedType or None
        self.prevo = data.prevo or ""
        self.tier = data.tier or ""
        self.doublesTier = data.doublesTier or ""
        self.natDexTier = data.natDexTier or ""
        self.evos = data.evos or []
        self.evoType = data.evoType or None
        self.evoMove = data.evoMove or None
        self.evoLevel = data.evoLevel or None
        self.nfe = data.nfe or False
        self.eggGroups = data.eggGroups or []
        self.canHatch = data.canHatch or False
        self.gender = data.gender or ""
        self.genderRatio = data.genderRatio or (
            {"M": 1, "F": 0}
            if self.gender == "M"
            else (
                {"M": 0, "F": 1}
                if self.gender == "F"
                else {"M": 0, "F": 0} if self.gender == "N" else {"M": 0.5, "F": 0.5}
            )
        )
        self.requiredItem = data.requiredItem or None
        self.requiredItems = self.requiredItems or (
            [self.requiredItem] if self.requiredItem else None
        )
        self.baseStats = data.baseStats or {
            "hp": 0,
            "atk": 0,
            "def": 0,
            "spa": 0,
            "spd": 0,
            "spe": 0,
        }
        self.bst = (
            self.baseStats["hp"]
            + self.baseStats["atk"]
            + self.baseStats["def"]
            + self.baseStats["spa"]
            + self.baseStats["spd"]
            + self.baseStats["spe"]
        )
        self.weightkg = data.weightkg or 0
        self.weighthg = self.weightkg * 10
        self.heightm = data.heightm or 0
        self.color = data.color or ""
        self.tags = data.tags or []
        self.unreleasedHidden = data.unreleasedHidden or False
        self.maleOnlyHidden = bool(data.maleOnlyHidden)
        self.maxHP = data.maxHP or None
        self.isMega = (
            bool(self.forme and self.forme in ["Mega", "Mega-X", "Mega-Y"]) or None
        )
        # self.canGigantamax = data.canGigantamax or None
        # self.gmaxUnreleased = bool(data.gmaxUnreleased)
        # self.cannotDynamax = bool(data.cannotDynamax)
        self.battleOnly = data.battleOnly or (self.baseSpecies if self.isMega else None)
        self.changesFrom = data.changesFrom or (
            self.battleOnly if self.battleOnly != self.baseSpecies else self.baseSpecies
        )
        if isinstance(data.changesFrom, list):
            self.changesFrom = data.changesFrom[0]

        self.gen = 0
        # if not hasattr(self, "gen") and self.num >= 1:
        #     if self.num >= 906 or "Paldea" in self.forme:
        #         self.gen = 9
        #     elif self.num >= 810 or any(
        #         forme in self.forme for forme in ["Gmax", "Galar", "Galar-Zen", "Hisui"]
        #     ):
        #         self.gen = 8
        #     elif (
        #         self.num >= 722
        #         or self.forme.startswith("Alola")
        #         or self.forme == "Starter"
        #     ):
        #         self.gen = 7
        #     elif self.forme == "Primal":
        #         self.gen = 6
        #         self.isPrimal = True
        #         self.battleOnly = self.baseSpecies
        #     elif self.num >= 650 or self.isMega:
        #         self.gen = 6
        #     elif self.num >= 494:
        #         self.gen = 5
        #     elif self.num >= 387:
        #         self.gen = 4
        #     elif self.num >= 252:
        #         self.gen = 3
        #     elif self.num >= 152:
        #         self.gen = 2
        #     else:
        #         self.gen = 1

    pass


class Learnset:
    effectType: Literal["Learnset"]
    pass
