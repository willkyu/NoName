from typing import Literal

from sim.globalTypes import *
from sim.dexData import BasicEffect
from utils.utils import Utils


class RuleTable:
    pass


class Format(BasicEffect):
    mod: str
    #: Name of the team generator algorithm, if this format uses
    #: random/fixed teams. None if players can bring teams.
    team: str | None
    effectType: FormatEffectType
    debug: bool
    #: Whether or not a format will update ladder points if searched
    #: for using the "Battle!" button.
    #: (Challenge and tournament games will never update ladder points.)
    #: (Defaults to `True`.)
    rated: bool | str
    #: Game type.
    gameType: GameType
    #: Number of players, based on game type, for convenience
    playerCount: Literal[2, 4]
    #: list of rule names.
    ruleset: list[str]
    #: Base list of rule names as specified in "./config/formats.ts".
    #: Used in a custom format to correctly display the altered ruleset.
    baseRuleset: list[str]
    #: list of banned effects.
    banlist: list[str]
    #: list of effects that aren't completely banned.
    restricted: list[str]
    #: list of inherited banned effects to override.
    unbanlist: list[str]
    #: list of ruleset and banlist changes in a custom format.
    customRules: list[str] | None
    #: Table of rule names and banned effects.
    ruleTable: RuleTable | None
    #: An optional function that runs at the start of a battle.
    onBegin: function
    noLog: bool

    #: Only applies to rules, not formats
    hasValue: bool | str | None
    onValidateRule: function
    #: ID of rule that can't be combined with this rule
    mutuallyExclusiveWith: str | None

    battle: ModdedBattleScriptsData | None
    non: ModdedBattleNon | None
    queue: ModdedBattleQueue | None
    field: ModdedField | None
    actions: ModdedBattleActions | None
    challengeShow: bool | None
    searchShow: bool | None
    bestOfDefault: bool | None
    threads: list[str] | None

    tournamentShow: bool | None
    checkCanLearn: function
    getEvoFamily: function
    getSharedPower: function
    getSharedItems: function
    onChangeSet: function
    onModifySpeciesPriority: number | None
    onModifySpecies: function
    onBattleStart: function
    onTeamPreview: function
    onValidateSet: function
    onValidateTeam: function
    validateSet: function
    validateTeam: function
    section: str | None
    column: number | None

    def __init__(self, data: object):
        super().__init__(data)
        self.__dict__.update(data.__dict__)
        data = self

        self.mod = Utils.getString(self.mod)
        self.effectType = Utils.getString(self.effectType)
        self.debug = bool(self.debug)
        self.rated = (
            self.rated if isinstance(self.rated, str) else self.rated is not False
        )
        self.ruleTable = None
        self.noLog = bool(self.noLog)
        self.playerCount = 4 if self.gameType in ["multi", "freeforall"] else 2
