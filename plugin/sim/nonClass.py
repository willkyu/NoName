from typing import Literal
from __future__ import annotations

from sim.battle import Battle
from sim.side import Side
from sim.globalTypes import *
from sim.dexSpecies import Species


class NonDex(object):
    def __init__(self) -> None:
        pass


class NonEntity:
    name: str  # Nickname
    masterId: str
    species: str
    item: str
    ability: str
    moves: list[str]
    nature: str
    gender: str
    evs: StatsTable
    ivs: StatsTable
    level: int
    shiny: bool | None
    happiness: int | None  # Friendship

    hpType: str | None  # HiddenPower


class MoveSlot:
    """
    A Pokemon's move slot.
    """

    id: ID
    move: str
    pp: int
    maxpp: int
    target: str | None
    disabled: bool | str
    disabledSource: str | None
    used: bool
    virtual: bool | None


class NONBattleEntity:
    side: Side
    battle: Battle
    entity: NonEntity
    name: str
    fullname: str
    level: int
    gender: GenderName
    happiness: number
    baseHpType: str
    baseHpPower: number

    baseMoveSlots: list[MoveSlot]
    moveSlots: list[MoveSlot]

    hpType: str
    hpPower: number

    """
     * Index of `pokemon.side.pokemon` and `pokemon.side.active`, which are
	 * guaranteed to be the same for active pokemon. Note that this isn't
	 * its field position in multi battles - use `getSlot()` for that.
    """
    position: number
    details: str

    baseSpecies: Species
    species: Species
    speciesState: EffectState

    status: ID
    statusState: EffectState
    volatiles: object
    showCure: bool | None

    """
     * These are the basic stats that appear on the in-game stats screen:
	 * calculated purely from the species base stats, level, IVs, EVs,
	 * and Nature, before modifications from item, ability, etc.
	 *
	 * Forme changes affect these, but Transform doesn't.
    """
    baseStoredStats: StatsTable

    """
     * These are pre-modification stored stats in-battle. At switch-in,
	 * they're identical to `baseStoredStats`, but can be temporarily changed
	 * until switch-out by effects such as Power Trick and Transform.
	 *
	 * Stat multipliers from abilities, items, and volatiles, such as
	 * Solar Power, Choice Band, or Swords Dance, are not stored in
	 * `storedStats`, but applied on top and accessed by `pokemon.getStat`.
	 *
	 * (Except in Gen 1, where stat multipliers are stored, leading
	 * to several famous glitches.)
    """
    storedStats: StatsExceptHPTable
    # boosts: BoostsTable

    baseAbility: ID
    ability: ID
    abilityState: EffectState

    item: ID
    itemState: EffectState
    lastItem: ID
    usedItemThisTurn: bool
    ateBerry: bool

    trapped: Literal[True, False, "hidden"]
    maybeTrapped: bool
    maybeDisabled: bool

    illusion: NONBattleEntity
    transformed: bool

    maxhp: int
    baseMaxhp: int
    hp: int
    fainted: bool
    faintQueued: bool
    subFainted: bool | None

    types: list[str]
    addedType: str
    knownType: bool
    apparentType: str

    """
     * If the switch is called by an effect with a special switch
	 * message, like U-turn or Baton Pass, this will be the ID of
	 * the calling effect.
    """
    switchFlag: ID | bool
    forceSwitchFlag: bool
    skipBeforeSwitchOutEventFlag: bool
    draggedIn: number | None
    newlySwitched: bool
    beingCalledBack: bool

    lastMove: ActiveMove | None

    """
     * The result of the last move used on the previous turn by this
	 * Pokemon. Stomping Tantrum checks this property for a value of false
	 * when determine whether to double its power, but it has four
	 * possible values:
	 *
	 * 0 indicates this Pokemon was not active last turn. It should
	 * not be used to indicate that a move was attempted and failed, either
	 * in a way that boosts Stomping Tantrum or not.
	 *
	 * None indicates that the Pokemon's move was skipped in such a way
	 * that does not boost Stomping Tantrum, either from having to recharge
	 * or spending a turn trapped by another Pokemon's Sky Drop.
	 *
	 * false indicates that the move completely failed to execute for any
	 * reason not mentioned above, including missing, the target being
	 * immune, the user being immobilized by an effect such as paralysis, etc.
	 *
	 * true indicates that the move successfully executed one or more of
	 * its effects on one or more targets, including hitting with an attack
	 * but dealing 0 damage to the target in cases such as Disguise, or that
	 * the move was blocked by one or more moves such as Protect.
    """
    moveLastTurnResult: Literal[True, False, 0, None]

    """
     * The result of the most recent move used this turn by this Pokemon.
	 * At the start of each turn, the value stored here is moved to its
	 * counterpart, moveLastTurnResult, and this property is reinitialized
	 * to undefined. This property can have one of four possible values:
	 *
	 * 0 indicates that this Pokemon has not yet finished an
	 * attempt to use a move this turn. As this value is only overwritten
	 * after a move finishes execution, it is not sufficient for an event
	 * to examine only this property when checking if a Pokemon has not
	 * moved yet this turn if the event could take place during that
	 * Pokemon's move.
	 *
	 * None indicates that the Pokemon's move was skipped in such a way
	 * that does not boost Stomping Tantrum, either from having to recharge
	 * or spending a turn trapped by another Pokemon's Sky Drop.
	 *
	 * false indicates that the move completely failed to execute for any
	 * reason not mentioned above, including missing, the target being
	 * immune, the user being immobilized by an effect such as paralysis, etc.
	 *
	 * true indicates that the move successfully executed one or more of
	 * its effects on one or more targets, including hitting with an attack
	 * but dealing 0 damage to the target in cases such as Disguise. It can
	 * also mean that the move was blocked by one or more moves such as
	 * Protect. Uniquely, this value can also be true if this Pokemon mega
	 * evolved or ultra bursted this turn, but in that case the value should
	 * always be overwritten by a move action before the end of that turn.
    """
    moveThisTurnResult: Literal[True, False, 0, None]

    hurtThisTurn: number | None
    lastDamage: int
    attackedBy: list[Attacker]
    timesAttacked: int

    isActive: bool
    activeTurns: number

    """
     * This is for Fake-Out-likes specifically - it mostly counts how many move
	 * actions you've had since the last time you switched in, so 1/turn normally,
	 * +1 for Dancer/Instruct, -1 for shifting/Sky Drop.
	 *
	 * Incremented before the move is used, so the first move use has
	 * `activeMoveActions === 1`.
	 *
	 * Unfortunately, Truant counts Mega Evolution as an action and Fake
	 * Out doesn't, meaning that Truant can't use this number.
    """
    activeMoveActions: number
    previouslySwitchedIn: number
    truantTurn: bool

    # Have this pokemon's Start events run yet? (Start events run every switch-in)
    isStarted: bool
    duringMove: bool

    weighthg: number
    speed: number
    abilityOrder: number

    canSpecialEvo: str | None

    staleness: Literal["internal", "external"] | None
    pendingStaleness: Literal["internale", "external"] | None
    volatileStaleness: Literal["external"] | None

    # An object for storing untyped data, for mods to use.
    m: object

    def __init__(self, nonSet: str | NonEntity, side: Side) -> None:
        self.side = side
        self.battle = side.battle

        self.m = {}
        self.baseSpecies = None

        pokemonScripts = self.battle.format_.non or self.battle.dex.data.Scripts.non
        if pokemonScripts:
            self.__dict__.update(pokemonScripts.__dict__)
        if isinstance(nonSet, str):
            nonSet = {"name": nonSet}
            self.baseSpecies = self.battle.dex.species.get(nonSet["name"])
        else:
            self.baseSpecies = self.battle.dex.species.get(nonSet.species)

        if self.baseSpecies is None:
            raise ValueError("Unidentified species: {}".format(self.baseSpecies.name))
        self.nonSet = nonSet

        self.species = self.baseSpecies
        if nonSet.name == nonSet.species or not self.name:
            nonSet.name = self.baseSpecies.baseSpecies

        self.speciesState = {"id": self.species.id}

        self.name = nonSet.name.substr(0, 20)

        # TODO


class EffectState:
    duration: number | any
