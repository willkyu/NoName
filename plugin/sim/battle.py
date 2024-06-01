"""
* Simulator Battle
* Following Pokemon Showdown - http:#pokemonshowdown.com/
*
* This file is where the battle simulation itself happens.
*
* The most important part of the simulation is the event system:
* see the `runEvent` function definition for details.
*
* General battle mechanics are in `battle-actions`; move-specific,
* item-specific, etc mechanics are in the corresponding file in
* `data`.
"""

import json
import math
import re
from __future__ import annotations
import time
from typing import Tuple

from sim.battleActions import BattleActions
from utils.utils import Utils
from sim.side import Side
from sim.nonClass import EffectState, NONBattleEntity
from sim.globalTypes import *
from sim.dexFormat import Format
from sim.state import State
from sim.dexSpecies import Species
from sim.dexAbility import Ability
from sim.dexMoves import ActiveMove, Move
from sim.dexConditions import Condition


def extractChannelMessages(message, channelIds):
    channelIdSet = set(channelIds)
    channelMessages: ChannelMessages = {
        -1: [],
        0: [],
        1: [],
        2: [],
        3: [],
        4: [],
    }

    for lineMatch, playerMatch, secretMessage, sharedMessage in re.findall(
        splitRegex, message
    ):
        player = int(playerMatch) if playerMatch else 0
        for channelId in channelIdSet:
            line = lineMatch
            if player:
                line = (
                    secretMessage
                    if channelId == -1 or player == channelId
                    else sharedMessage
                )
                if not line:
                    continue
            channelMessages[channelId].append(line)

    return channelMessages


class BattleOptions:
    format_: Format | None
    formatid: ID

    send: function | None
    prng: PRNG | None
    seed: PRNGSeed | None
    rated: bool | str | None
    p1: PlayerOptions | None
    p2: PlayerOptions | None
    p3: PlayerOptions | None
    p4: PlayerOptions | None
    debug: bool | None
    forceRandomChance: bool | None
    deserialized: bool | None
    strictChoices: bool | None


class EventListenerWithoutPriority:
    effect: Effect
    target: NONBattleEntity
    index: number
    callback: function | None
    state: EffectState | None
    end: function | None
    endCallArgs: list | None
    effectHolder: Side | Field | Battle | NONBattleEntity


class EventListener(EventListenerWithoutPriority):
    order: number | Literal[False]
    priority: number
    subOrder: number
    speed: number | None


Part = str | number | bool | NONBattleEntity | Side | Effect | Move | None | Literal[0]


class Battle:
    battleId: ID
    debugMode: bool
    forceRandomChance: bool | None
    deserialized: bool
    strictChoices: bool
    format_: Format
    formatData: EffectState
    gameType: GameType

    """
  	 * The number of active pokemon per half-field.
	 * See header comment in side.ts for details.
    """
    activePerHalf: Literal[1, 2, 3]
    field: Field
    sides: list[Side]  # [Side, Side] | [Side, Side, Side, Side]
    prngSeed: PRNGSeed

    dex: ModdedDex
    gen: number
    ruleTable: object  # Dex.RuleTable
    prng: PRNG
    rated: bool | str
    reportExactHP: bool
    supportCancel: bool

    actions: BattleActions
    queue: BattleQueue
    faintQueue: dict
    log: list[str]
    inputLog: list[str]
    messageLog: list[str]
    sentLogPos: number
    sentEnd: bool

    requestState: RequestState
    turn: number
    midTurn: bool
    started: bool
    ended: bool
    winner: str | None

    effect: Effect
    effectState: EffectState

    event: object
    events: object | None
    eventDepth: number

    activeMove: ActiveMove | None
    activeNon: NONBattleEntity | None
    activeTarget: NONBattleEntity | None

    lastMove: ActiveMove | None
    lastSuccessfulMoveThisTurn: ID | None
    lastMoveLine: number

    teamGenerator: object

    def __init__(self, options: BattleOptions):
        self.log = []
        self.add("t:", math.floor(time.time()))
        format_ = options.format_ or Dex.formats.get(options.formatid, True)
        self.format_ = format_
        self.dex = Dex.forFormat(format_)
        self.gen = self.dex.gen
        self.ruleTable = self.dex.formats.getRuleTable(format_)

        self.trunc = self.dex.trunc
        self.clampIntRange = Utils.clampIntRange

        for i in self.dex.data.Scripts:
            entry = self.dex.data.Scripts[i]
            if isinstance(entry, Callable):
                setattr(self, i, entry)
        if format_.battle:
            self.__dict__.update(format_.battle.__dict__)

        self.battleId = ""
        self.debugMode = format_.debug or options.debug

        self.forceRandomChance = (
            options.forceRandomChance
            if self.debugMode and isinstance(options.forceRandomChance, bool)
            else None
        )
        self.deserialized = options.deserialized
        self.strictChoices = options.strictChoices
        self.formatData = {"id": format_.id}
        self.gameType = format_.gameType or "singles"
        self.field = Field(self)
        self.sides = [None] * format_.playerCount
        self.activePerHalf = (
            3
            if self.gameType == "triples"
            else 2 if format_.playerCount > 2 or self.gameType == "doubles" else 1
        )
        self.prng = options.prng or PRNG(options.seed or None)
        self.prngSeed = self.prng.startingSeed.slice()
        self.rated = options.rated
        self.reportExactHP = format_.debug
        self.reportPercentages = False
        self.supportCancel = False

        self.queue = BattleQueue(self)
        self.actions = BattleActions(self)
        self.faintQueue = []

        self.inputLog = []
        self.messageLog = []
        self.sentLogPos = 0
        self.sentEnd = False

        self.requestState = ""
        self.turn = 0
        self.midTurn = False
        self.started = False
        self.ended = False

        self.effect = {"id": ""}
        self.effectState = {"id": ""}

        self.event = {"id": ""}
        self.events = None
        self.eventDepth = 0

        self.activeMove = None
        self.activeNon = None
        self.activeTarget = None

        self.lastMove = None
        self.lastMoveLine = -1
        self.lastSuccessfulMoveThisTurn = None
        self.lastDamage = 0
        self.abilityOrder = 0
        self.quickClawRoll = False

        self.teamGenerator = None

        self.send = options.send or None

        inputOptions = {"formatid": options.formatid, "seed": self.prng.seed}
        if self.rated:
            inputOptions["rated"] = self.rated
        self.inputLog.append(">start " + json.dumps(inputOptions))
        self.add("gametype", self.gameType)

        # timing is early enough to hook into ModifySpecies event
        for rule in self.ruleTable.keys():
            if rule[0] in ("+", "*", "-", "!"):
                continue
            subFormat = self.dex.formats.get(rule)
            if subFormat.exists:
                hasEventHandler = any(
                    # skip event handlers that are handled elsewhere
                    val.startswith("on")
                    and val
                    not in [
                        "onBegin",
                        "onTeamPreview",
                        "onBattleStart",
                        "onValidateRule",
                        "onValidateTeam",
                        "onChangeSet",
                        "onValidateSet",
                    ]
                    for val in subFormat
                )
                if hasEventHandler:
                    self.field.addPseudoWeather(rule)

        sides = ["p1", "p2", "p3", "p4"]
        for side in sides:
            if side in options:
                self.setPlayer(side, options[side])

        pass

    def add(self, *parts: Part | Callable[[], Tuple[SideID, str, str]]):
        if not any(isinstance(part, Callable) for part in parts):
            self.log.append(f"|{'|'.join(map(str, parts))}")
            return

        side: SideID | None = None
        secret = []
        shared = []
        for part in parts:
            if isinstance(part, Callable):
                split = part()
                if side and side != split[0]:
                    raise ValueError("Multiple sides passed to add")
                side = split[0]
                secret.append(split[1])
                shared.append(split[2])
            else:
                secret.append(part)
                shared.append(part)
        self.addSplit(side, secret, shared)

    def addSplit(
        self, side: SideID, secret: list[Part] | None, shared: list[Part] | None
    ):
        self.log.append("|split|{}".format(side))
        self.add(secret)
        if shared:
            self.add(shared)
        else:
            self.log.append("")
        pass

    def toJSON(self):
        return State.serializeBattle(self)

    @staticmethod
    def fromJSON(serialized: str | object) -> Battle:
        return State.deserializeBattle(serialized)

    @property
    def p1(self):
        return self.sides[0]

    @property
    def p2(self):
        return self.sides[1]

    @property
    def p3(self):
        return self.sides[2]

    @property
    def p4(self):
        return self.sides[3]

    def __str__(self):
        return f"Battle: {self.format_}"

    def random(self, m: number | None, n: number | None):
        return self.prng.next(m, n)

    def randomChance(self, numerator: number, denominator: number):
        if self.forceRandomChance is not None:
            return self.forceRandomChance
        return self.prng.randomChance(numerator, denominator)

    def sample(self, items):
        return self.prng.sample(items)

    def suppressingAbility(self, target: NONBattleEntity | None):
        # 技能是否无视特性
        return (
            self.active_pokemon
            and self.active_pokemon.is_active
            # and (self.active_pokemon != target or self.gen < 8)
            and self.active_move
            and self.active_move.ignore_ability
            and not (target.has_item("Ability Shield") if target else False)
        )

    def setActiveMove(
        self,
        move: ActiveMove | None,
        non: NONBattleEntity | None,
        target: NONBattleEntity | None,
    ):
        self.activeMove = move or None
        self.activeNon = non or None
        self.activeTarget = target or non or None

    def clearActiveMove(self, failed: bool | None):
        if self.activeMove:
            if not failed:
                self.lastMove = self.activeMove
            self.activeMove = None
            self.activeNon = None
            self.activeTarget = None

    def updateSpeed(self):
        for non in self.getAllActive():
            non.updateSpeed()

    """
     * The default sort order for actions, but also event listeners.
	 *
	 * 1. Order, low to high (default last)
	 * 2. Priority, high to low (default 0)
	 * 3. Speed, high to low (default 0)
	 * 4. SubOrder, low to high (default 0)
	 *
	 * Doesn't reference `this` so doesn't need to be bound.
    """

    @staticmethod
    def comparePriority(a, b):
        return (
            -((b.get("order", 4294967296) - a.get("order", 4294967296)))
            or ((b.get("priority", 0) - a.get("priority", 0)))
            or ((b.get("speed", 0) - a.get("speed", 0)))
            or -((b.get("sub_order", 0) - a.get("sub_order", 0)))
            or 0
        )

    @staticmethod
    def compareRedirectOrder(a, b):
        return (
            ((b.get("priority", 0) - a.get("priority", 0)))
            or ((b.get("speed", 0) - a.get("speed", 0)))
            or (
                -(
                    b.get("effect_holder").ability_order
                    - a.get("effect_holder").ability_order
                )
                if a.get("effect_holder") and b.get("effect_holder")
                else 0
            )
            or 0
        )

    @staticmethod
    def compareLeftToRightOrder(a, b):
        return (
            -((b.get("order", 4294967296) - a.get("order", 4294967296)))
            or ((b.get("priority", 0) - a.get("priority", 0)))
            or -((b.get("index", 0) - a.get("index", 0)))
            or 0
        )

    def speedSort(self, lst: list, comparator: function = None):
        # Sort a list, resolving speed ties the way the games do.
        if len(lst) < 2:
            return
        if comparator is None:
            comparator = self.comparePriority

        # This is a Selection Sort - not the fastest sort in general, but
        # actually faster than QuickSort for small arrays like the ones
        # `speedSort` is used for.
        # More importantly, it makes it easiest to resolve speed ties
        # properly.
        index = 0
        while index + 1 < len(lst):
            nextIndex = [index]
            for i in range(index + 1, len(lst)):
                delta = comparator(lst[nextIndex[0]], lst[i])
                if delta < 0:
                    continue
                if delta > 0:
                    nextIndex = [i]
                if delta == 0:
                    nextIndex.append(i)
            for i in range(len(nextIndex)):
                idx = nextIndex[i]
                if idx != index + i:
                    lst[index + i], lst[idx] = lst[idx], lst[index + i]
            if len(nextIndex) > 1:
                self.prng.shuffle(lst, index, index + len(nextIndex))

            index += len(nextIndex)

    def eachEvent(self, eventid: str, effect: Effect | None, relayVar: bool | None):
        # * Runs an event with no source on each NON on the field, in Speed order.
        actives = self.getAllActive()
        if not effect and self.effect:
            effect = self.effect

        self.speedSort(actives, lambda a, b: b.speed - a.speed)

        for non in actives:
            self.runEvent(eventid, non, None, effect, relayVar)

        if eventid == "Weather":
            # TODO in PS: further research when updates happen
            self.eachEvent("Update")

    def residualEvent(self, eventid: str, relayVar: any | None):
        """
        * Runs an event with no source on each effect on the field, in Speed order.
            *
            * Unlike `eachEvent`, this contains a lot of other handling and is intended only for the residual step.
        """
        callbackName = f"on{eventid}"
        handlers = self.findBattleEventHandlers(callbackName, "duration")
        handlers.extend(
            self.findFieldEventHandlers(self.field, f"onField{eventid}", "duration")
        )
        for side in self.sides:
            if side.n < 2 or not side.allySide:
                handlers.extend(
                    self.findSideEventHandlers(side, f"onSide{eventid}", "duration")
                )
            for active in side.active:
                if not active:
                    continue
                handlers.extend(
                    self.findNonEventHandlers(active, callbackName, "duration")
                )
                handlers.extend(
                    self.findSideEventHandlers(side, callbackName, None, active)
                )
                handlers.extend(
                    self.findFieldEventHandlers(self.field, callbackName, None, active)
                )

        self.speedSort(handlers)

        while handlers:
            handler = handlers.pop(0)
            effect = handler.effect
            if handler.effectHolder.fainted:
                continue
            if handler.end and handler.state and handler.state.duration:
                handler.state.duration -= 1
                if not handler.state.duration:
                    endCallArgs = handler.endCallArgs or [
                        handler.effectHolder,
                        effect.id,
                    ]
                    handler.end(*endCallArgs)
                    if self.ended:
                        return
                    continue
            handlerEventid = eventid
            if handler.effectHolder.sideConditions:
                handlerEventid = f"Side{eventid}"
            if handler.effectHolder.pseudoWeather:
                handlerEventid = f"Field{eventid}"
            if handler.callback:
                self.singleEvent(
                    handlerEventid,
                    effect,
                    handler.state,
                    handler.effectHolder,
                    None,
                    None,
                    relayVar,
                    handler.callback,
                )
            self.faintMessages()
            if self.ended:
                return

    # * The entire event system revolves around this function and runEvent.
    def singleEvent(
        self,
        eventid: str,
        effect: Effect,
        state: dict | None,
        target: str | NONBattleEntity | Side | Field | Battle | None,
        source: str | NONBattleEntity | Effect | bool | None = None,
        sourceEffect: Effect | str | None = None,
        relayVar: any = None,
        customCallback: Callable | None = None,
    ):
        if self.eventDepth >= 8:
            self.add("message", "STACK LIMIT EXCEEDED")
            self.add("message", "PLEASE REPORT IN BUG THREAD")
            self.add("message", f"Event: {eventid}")
            self.add("message", f"Parent event: {self.event.id}")
            raise RuntimeError("Stack overflow")

        if len(self.log) - self.sentLogPos > 1000:
            self.add("message", "LINE LIMIT EXCEEDED")
            self.add("message", "PLEASE REPORT IN BUG THREAD")
            self.add("message", f"Event: {eventid}")
            self.add("message", f"Parent event: {self.event.id}")
            raise RuntimeError("Infinite loop")

        hasRelayVar = True
        if relayVar is None:
            relayVar = True
            hasRelayVar = False

        if (
            effect.effectType == "Status"
            and isinstance(target, NONBattleEntity)
            and target.status != effect.id
        ):
            return relayVar
        if (
            eventid not in ["Start", "TakeItem", "Primal"]
            and effect.effectType == "Item"
            and isinstance(target, NONBattleEntity)
            and target.ignoringItem()
        ):
            self.debug(f"{eventid} handler suppressed by Embargo, Klutz or Magic Room")
            return relayVar

        if (
            eventid != "End"
            and effect.effectType == "Ability"
            and isinstance(target, NONBattleEntity)
            and target.ignoringAbility()
        ):
            self.debug(
                f"{eventid} handler suppressed by Gastro Acid or Neutralizing Gas"
            )
            return relayVar

        if (
            effect.effectType == "Weather"
            and eventid not in ["FieldStart", "FieldResidual", "FieldEnd"]
            and self.field.suppressingWeather()
        ):
            self.debug(f"{eventid} handler suppressed by Air Lock")
            return relayVar

        callback = customCallback or getattr(effect, f"on{eventid}", None)
        if callback is None:
            return relayVar

        parentEffect = self.effect
        parentEffectState = self.effectState
        parentEvent = self.event

        self.effect = effect
        self.effectState = state or {}
        self.event = {
            "id": eventid,
            "target": target,
            "source": source,
            "effect": sourceEffect,
        }
        self.eventDepth += 1

        args = [target, source, sourceEffect]
        if hasRelayVar:
            args.insert(0, relayVar)

        returnVal = None
        if callable(callback):
            returnVal = callback(*args)
        else:
            returnVal = callback

        self.eventDepth -= 1
        self.effect = parentEffect
        self.effectState = parentEffectState
        self.event = parentEvent

        return returnVal if returnVal is not None else relayVar

    """
     * runEvent is the core of Pokemon Showdown's event system.
	 *
	 * Basic usage
	 * ===========
	 *
	 *   this.runEvent('Blah')
	 * will trigger any onBlah global event handlers.
	 *
	 *   this.runEvent('Blah', target)
	 * will additionally trigger any onBlah handlers on the target, onAllyBlah
	 * handlers on any active pokemon on the target's team, and onFoeBlah
	 * handlers on any active pokemon on the target's foe's team
	 *
	 *   this.runEvent('Blah', target, source)
	 * will additionally trigger any onSourceBlah handlers on the source
	 *
	 *   this.runEvent('Blah', target, source, effect)
	 * will additionally pass the effect onto all event handlers triggered
	 *
	 *   this.runEvent('Blah', target, source, effect, relayVar)
	 * will additionally pass the relayVar as the first argument along all event
	 * handlers
	 *
	 * You may leave any of these null. For instance, if you have a relayVar but
	 * no source or effect:
	 *   this.runEvent('Damage', target, null, null, 50)
	 *
	 * Event handlers
	 * ==============
	 *
	 * Items, abilities, statuses, and other effects like SR, confusion, weather,
	 * or Trick Room can have event handlers. Event handlers are functions that
	 * can modify what happens during an event.
	 *
	 * event handlers are passed:
	 *   function (target, source, effect)
	 * although some of these can be blank.
	 *
	 * certain events have a relay variable, in which case they're passed:
	 *   function (relayVar, target, source, effect)
	 *
	 * Relay variables are variables that give additional information about the
	 * event. For instance, the damage event has a relayVar which is the amount
	 * of damage dealt.
	 *
	 * If a relay variable isn't passed to runEvent, there will still be a secret
	 * relayVar defaulting to `true`, but it won't get passed to any event
	 * handlers.
	 *
	 * After an event handler is run, its return value helps determine what
	 * happens next:
	 * 1. If the return value isn't `undefined`, relayVar is set to the return
	 *    value
	 * 2. If relayVar is falsy, no more event handlers are run
	 * 3. Otherwise, if there are more event handlers, the next one is run and
	 *    we go back to step 1.
	 * 4. Once all event handlers are run (or one of them results in a falsy
	 *    relayVar), relayVar is returned by runEvent
	 *
	 * As a shortcut, an event handler that isn't a function will be interpreted
	 * as a function that returns that value.
	 *
	 * You can have return values mean whatever you like, but in general, we
	 * follow the convention that returning `false` or `null` means
	 * stopping or interrupting the event.
	 *
	 * For instance, returning `false` from a TrySetStatus handler means that
	 * the pokemon doesn't get statused.
	 *
	 * If a failed event usually results in a message like "But it failed!"
	 * or "It had no effect!", returning `null` will suppress that message and
	 * returning `false` will display it. Returning `null` is useful if your
	 * event handler already gave its own custom failure message.
	 *
	 * Returning `undefined` means "don't change anything" or "keep going".
	 * A function that does nothing but return `undefined` is the equivalent
	 * of not having an event handler at all.
	 *
	 * Returning a value means that that value is the new `relayVar`. For
	 * instance, if a Damage event handler returns 50, the damage event
	 * will deal 50 damage instead of whatever it was going to deal before.
	 *
	 * Useful values
	 * =============
	 *
	 * In addition to all the methods and attributes of Dex, Battle, and
	 * Scripts, event handlers have some additional values they can access:
	 *
	 * this.effect:
	 *   the Effect having the event handler
	 * this.effectState:
	 *   the data store associated with the above Effect. This is a plain Object
	 *   and you can use it to store data for later event handlers.
	 * this.effectState.target:
	 *   the Pokemon, Side, or Battle that the event handler's effect was
	 *   attached to.
	 * this.event.id:
	 *   the event ID
	 * this.event.target, this.event.source, this.event.effect:
	 *   the target, source, and effect of the event. These are the same
	 *   variables that are passed as arguments to the event handler, but
	 *   they're useful for functions called by the event handler.
    """

    def runEvent():
        pass

    def getAllActive(self) -> list[NONBattleEntity]:
        nonList = []
        for side in self.sides:
            for non in side.active:
                if non and not non.fainted:
                    nonList.append(non)
        return nonList
