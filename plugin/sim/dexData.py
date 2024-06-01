import re

from sim.globalTypes import *


def toID(text: any) -> str:
    # The sucrase transformation of optional chaining is too expensive to be used in a hot function like this.
    # eslint-disable @typescript-eslint/prefer-optional-chain
    if text and hasattr(text, "id"):
        text = text.id
    elif text and hasattr(text, "userid"):
        text = text.userid
    elif text and hasattr(text, "roomid"):
        text = text.roomid
    if not isinstance(text, (str, int)):
        return ""
    # eslint-enable @typescript-eslint/prefer-optional-chain
    return re.sub(r"[^a-z0-9]+", "", str(text).lower())


class BasicEffect(EffectData):
    """
    ID. This will be a lowercase version of the name with all the
    non-alphanumeric characters removed. So, for instance, "Mr. Mime"
    becomes "mrmime", and "Basculin-Blue-Striped" becomes
    "basculinbluestriped".
    """

    id: ID
    """
    Name. Currently does not support Unicode letters, so "Flabébé"
    is "Flabebe" and "Nidoran♀" is "Nidoran-F".
    """
    name: str
    """
    Full name. Prefixes the name with the effect type. For instance,
    Leftovers would be "item: Leftovers", confusion the status
    condition would be "confusion", etc.
    """
    fullname: str
    """ Effect type. """
    effectType: str
    """
    Does it exist? For historical reasons, when you use an accessor
    for an effect that doesn't exist, you get a dummy effect that
    doesn't do anything, and this field set to false.
    """
    exists: bool
    """
    Dex number? For a Pokemon, this is the National Dex number. For
    other effects, this is often an internal ID (e.g. a move
    number). Not all effects have numbers, this will be 0 if it
    doesn't. Nonstandard effects (e.g. CAP effects) will have
    negative numbers.
    """
    num: int
    """
    The generation of Pokemon game this was INTRODUCED (NOT
    necessarily the current gen being simulated.) Not all effects
    track generation; this will be 0 if not known.
    """
    gen: number
    """
    A shortened form of the description of this effect.
    Not all effects have this.
    """
    shortDesc: str
    """ The full description for this effect. """
    desc: str
    """
    Is this item/move/ability/pokemon nonstandard? Specified for effects
    that have no use in standard formats: made-up pokemon (CAP),
    glitches (MissingNo etc), Pokestar pokemon, etc.
    """
    isNonstandard: Nonstandard | None
    """ The duration of the condition - only for pure conditions. """
    duration: number | None
    """ Whether or not the condition is ignored by Baton Pass - only for pure conditions. """
    noCopy: bool
    """ Whether or not the condition affects fainted Pokemon. """
    affectsFainted: bool
    """ Moves only: what status does it set? """
    status: ID | None
    """ Moves only: what weather does it set? """
    weather: ID | None
    """ ??? """
    sourceEffect: str

    def __init__(self, data: object) -> None:
        super().__init__()
        self.exists = True
        self.__dict__.update(data.__dict__)

        pass
