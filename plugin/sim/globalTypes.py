from typing import Literal
from re import compile, MULTILINE

from sim.battleQueue import BattleQueue
from sim.dexItem import Item
from sim.field import Field

number = int | float
SideID = Literal["p1", "p2", "p3", "p4"]
RequestState = Literal["teampreview", "move", "switch", ""]
ChannelID = Literal[0, 1, 2, 3, 4]
ChannelMessages = dict[Literal[ChannelID, -1], list[str]]
Nonstandard = Literal[
    "Past", "Future", "Unobtainable", "CAP", "LGPE", "Custom", "Gigantamax"
]
ID = str | dict
FormatEffectType = Literal["Format", "Ruleset", "Rule", "ValidatorRule"]
GameType = Literal["singles", "doubles", "triples", "rotation", "multi", "freeforall"]
Action = Literal[
    "MoveAction", "SwitchAction", "TeamAction", "FieldAction", "PokemonAction"
]

splitRegex = compile("/^\|split\|p([1234])\n(.*)\n(.*)|.+", MULTILINE)


class EffectData:
    name: str | None
    desc: str | None
    duration: number | None
    effectType: str | None
    infiltrates: bool | None
    isNonstandard: Nonstandard | None
    shortDesc: str | None


class BattleScriptsData:
    gen: number


class ModdedBattleActions:
    """这里定义了规则哪些是允许操作的，以后的多规则可以拓展"""

    inherit: True | None
    afterMoveSecondaryEvent: function | None
    calcRecoilDamage: function | None
    canSpecialEvo: function | None
    forceSwitch: function | None
    getSpreadDamage: function | None
    hitStepAccuracy: function | None
    hitStepBreakProtect: function | None
    hitStepMoveHitLoop: function | None
    hitStepTryImmunity: function | None
    hitStepSteelBoosts: function | None
    hitStepTryHitEvent: function | None
    hitStepInvulnerabilityEvent: function | None
    hitStepTypeImmunity: function | None
    moveHit: function | None
    runAction: function | None
    runSpecialEvo: function | None
    runMove: function | None
    runMoveEffects: function | None
    runSwitch: function | None
    secondaries: function | None
    selfDrops: function | None
    spreadMoveHit: function | None
    switchIn: function | None
    targetTypeChoices: function | None
    tryMoveHit: function | None
    tryPrimaryHitEvent: function | None
    trySpreadMoveHit: function | None
    useMove: function | None
    useMoveInner: function | None
    getDamage: function | None
    modifyDamage: function | None


class ModdedBattleNon:
    inherit: True | None
    lostItemForDelibird: Item | None
    boostBy: function | None
    clearBoosts: function | None
    calculateStat: function | None
    modifier: function | None
    cureStatus: function | None
    silent: function | None
    deductPP: function | None
    amount: function | None
    target: function | None
    eatItem: function | None
    force: function | None
    source: function | None
    sourceEffect: function | None
    effectiveWeather: function | None
    formeChange: function | None
    isPermanent: function | None
    message: function | None
    hasType: function | None
    getAbility: function | None
    getActionSpeed: function | None
    getItem: function | None
    getMoveRequestData: function | None
    target: function | None
    disabled: function | None
    maybeDisabled: function | None
    trapped: function | None
    maybeTrapped: function | None
    canMegaEvo: function | None
    canUltraBurst: function | None
    canZMove: function | None
    getMoves: function | None
    lockedMove: function | None
    restrictData: function | None
    disabled: function | None
    disabledSource: function | None
    target: function | None
    pp: function | None
    maxpp: function | None
    getMoveTargets: function | None
    getStat: function | None
    unboosted: function | None
    unmodified: function | None
    fastReturn: function | None
    getTypes: function | None
    excludeAdded: function | None
    preterastallized: function | None
    getWeight: function | None
    hasAbility: function | None
    hasItem: function | None
    isGrounded: function | None
    modifyStat: function | None
    moveUsed: function | None
    targetLoc: function | None
    recalculateStats: function | None
    runEffectiveness: function | None
    runImmunity: function | None
    message: function | None
    setAbility: function | None
    setItem: function | None
    source: function | None
    effect: function | None
    setStatus: function | None
    takeItem: function | None
    transformInto: function | None
    useItem: function | None
    source: function | None
    sourceEffect: function | None
    ignoringAbility: function | None
    ignoringItem: function | None

    getLinkedMoves: function | None
    ignoreDisabled: function | None
    hasLinkedMove: function | None


class ModdedBattleQueue(BattleQueue):
    resolveAction: function | None


class ModdedField(Field):
    suppressingWeather: function | None


class ModdedBattleSide:
    canSpecialEvoNow: function | None
    chooseSwitch: function | None
    getChoice: function | None
    getRequestData: function | None


class ModdedBattleScriptsData(BattleScriptsData):
    inherit: str | None
    actions: ModdedBattleActions | None
    non: ModdedBattleNon | None
    queue: ModdedBattleQueue | None
    field: ModdedField | None
    side: ModdedBattleSide | None

    boost: function | None
    source: function | None
    effect: function | None
    isSecondary: function | None
    isSelf: function | None
    debug: function | None
    getActionSpeed: function | None
    init: function | None
    maybeTriggerEndlessBattleClause: function | None
    natureModify: function | None
    nextTurn: function | None
    runAction: function | None
    spreadModify: function | None
    start: function | None
    suppressingWeather: function | None
    trunc: function | None
    win: function | None
    side: function | None
    faintMessages: function | None
    lastFirst: function | None
    forceCheck: function | None
    checkWin: function | None
    tiebreak: function | None
    checkMoveMakesContact: function | None
    announcePads: function | None
    checkWin: function | None
    faintQueue: function | None
    pass
