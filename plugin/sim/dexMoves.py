from typing import Literal, TypedDict

from sim.dexData import BasicEffect, toID
from sim.dexAbility import Ability
from utils.utils import Utils
from sim.globalTypes import *
from sim.nonClass import NONBattleEntity

"""
* Describes the acceptable target(s) of a move.
* adjacentAlly - Only relevant to Doubles or Triples, the move only targets an ally of the user.
* adjacentAllyOrSelf - The move can target the user or its ally.
* adjacentFoe - The move can target a foe, but not (in Triples) a distant foe.
* all - The move targets the field or all Pokémon at once.
* allAdjacent - The move is a spread move that also hits the user's ally.
* allAdjacentFoes - The move is a spread move.
* allies - The move affects all active Pokémon on the user's team.
* allySide - The move adds a side condition on the user's side.
* allyTeam - The move affects all unfaLiteral[1,None]ed Pokémon on the user's team.
* any - The move can hit any other active Pokémon, not just those adjacent.
* foeSide - The move adds a side condition on the foe's side.
* normal - The move can hit one adjacent Pokémon of your choice.
* randomNormal - The move targets an adjacent foe at random.
* scripted - The move targets the foe that damaged the user.
* self - The move affects the user of the move.
"""
MoveTarget = Literal[
    "adjacentAlly",
    "adjacentAllyOrSelf",
    "adjacentFoe",
    "all",
    "allAdjacent",
    "allAdjacentFoes",
    "allies",
    "allySide",
    "allyTeam",
    "any",
    "foeSide",
    "normal",
    "randomNormal",
    "scripted",
    "self",
]


class MoveFlags(TypedDict, total=False):
    allyanim: Literal[1, None]  # The move plays its animation when used on an ally.
    bypasssub: Literal[1, None]  # Ignores a target's substitute.
    bite: Literal[
        1, None
    ]  # Power is multiplied by 1.5 when used by a Pokemon with the Ability Strong Jaw.
    bullet: Literal[1, None]  # Has no effect on Pokemon with the Ability Bulletproof.
    cantusetwice: Literal[
        1, None
    ]  # The user cannot select this move after a previous successful use.
    charge: Literal[1, None]  # The user is unable to make a move between turns.
    contact: Literal[1, None]  # Makes contact.
    dance: Literal[
        1, None
    ]  # When used by a Pokemon, other Pokemon with the Ability Dancer can attempt to execute the same move.
    defrost: Literal[
        1, None
    ]  # Thaws the user if executed successfully while the user is frozen.
    distance: Literal[
        1, None
    ]  # Can target a Pokemon positioned anywhere in a Triple Battle.
    failcopycat: Literal[1, None]  # Cannot be selected by Copycat.
    failencore: Literal[1, None]  # Encore fails if target used this move.
    failinstruct: Literal[1, None]  # Cannot be repeated by Instruct.
    failmefirst: Literal[1, None]  # Cannot be selected by Me First.
    failmimic: Literal[1, None]  # Cannot be copied by Mimic.
    futuremove: Literal[1, None]  # Targets a slot, and in 2 turns damages that slot.
    gravity: Literal[
        1, None
    ]  # Prevented from being executed or selected during Gravity's effect.
    heal: Literal[
        1, None
    ]  # Prevented from being executed or selected during Heal Block's effect.
    metronome: Literal[1, None]  # Can be selected by Metronome.
    mirror: Literal[1, None]  # Can be copied by Mirror Move.
    mustpressure: Literal[
        1, None
    ]  # Additional PP is deducted due to Pressure when it ordinarily would not.
    noassist: Literal[1, None]  # Cannot be selected by Assist.
    nonsky: Literal[
        1, None
    ]  # Prevented from being executed or selected in a Sky Battle.
    noparentalbond: Literal[1, None]  # Cannot be made to hit twice via Parental Bond.
    nosleeptalk: Literal[1, None]  # Cannot be selected by Sleep Talk.
    pledgecombo: Literal[
        1, None
    ]  # Gems will not activate. Cannot be redirected by Storm Drain / Lightning Rod.
    powder: Literal[
        1, None
    ]  # Has no effect on Pokemon which are Grass-type, have the Ability Overcoat, or hold Safety Goggles.
    protect: Literal[
        1, None
    ]  # Blocked by Detect, Protect, Spiky Shield, and if not a Status move, King's Shield.
    pulse: Literal[
        1, None
    ]  # Power is multiplied by 1.5 when used by a Pokemon with the Ability Mega Launcher.
    punch: Literal[
        1, None
    ]  # Power is multiplied by 1.2 when used by a Pokemon with the Ability Iron Fist.
    recharge: Literal[
        1, None
    ]  # If this move is successful, the user must recharge on the following turn and cannot make a move.
    reflectable: Literal[
        1, None
    ]  # Bounced back to the original user by Magic Coat or the Ability Magic Bounce.
    slicing: Literal[
        1, None
    ]  # Power is multiplied by 1.5 when used by a Pokemon with the Ability Sharpness.
    snatch: Literal[
        1, None
    ]  # Can be stolen from the original user and instead used by another Pokemon using Snatch.
    sound: Literal[1, None]  # Has no effect on Pokemon with the Ability Soundproof.
    wind: Literal[1, None]  # Activates the Wind Power and Wind Rider Abilities.


class HitEffect(TypedDict, total=False):
    onHit: dict
    boosts: BoostsTable | None
    status: str
    volatileStatus: str
    sideCondition: str
    slotCondition: str
    pseudoWeather: str
    terrain: str
    weather: str


class SecondaryEffect(HitEffect, total=False):
    chance: int
    ability: Ability
    dustproof: bool
    kingsrock: bool
    self: HitEffect


class MoveEventMethods(TypedDict):
    onDamagePriority: number | None
    onHit: dict

    pass


class MoveData(EffectData, MoveEventMethods, HitEffect):
    name: str
    pass


class ModdedMoveData(MoveData):
    pass


class Move(BasicEffect, MoveData):
    effectType: Literal["Move"]


class MoveHitData:
    pass


class MutableMove(BasicEffect, MoveData):
    pass


class RuinableMove(TypedDict):
    ruinedAtk: NONBattleEntity
    ruinedDef: NONBattleEntity
    ruinedSpA: NONBattleEntity
    ruinedSpD: NONBattleEntity


class ActiveMove(MutableMove, RuinableMove):
    name: str
    effectType: Literal["Move"]
    id: ID
    num: number
    weather: ID | None
    status: ID | None
    hit: number
    moveHitData: MoveHitData | None
    ability: Ability | None
    allies: list[NONBattleEntity]
    auraBooster: NONBattleEntity | None
    causedCrashDamage: bool | None
    forceStatus: ID | None
    hasAuraBreak: bool | None
    hasBounced: bool | None
    hasSheerForce: bool | None

    isExternal: bool | None
    lastHit: bool | None
    magnitude: bool | None
    negateSecondary: bool | None
    pranksterBoosted: bool | None
    selfDropped: bool
    selfSwitch: bool | Literal["copyvolatile", "shedtail"]
    spreadHit: bool | None
    statusRoll: str | None

    stellarBoosted: bool | None
    totalDamage: number | Literal[False] | None
    typeChangerBoosted: Effect | None
    willChangeForme: bool | None
    infiltrates: bool | None
