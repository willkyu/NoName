from plugin.sim.battle import Battle


class State:
    # REFERABLE is used to determine which objects are of the Referable type by
    # comparing their constructors. Unfortunately, we need to set this dynamically
    # due to circular module dependencies on Battle and Field instead
    # of simply initializing it as a const. See isReferable for where this
    # gets lazily created on demand.
    # eslint-disable-next-line @typescript-eslint/ban-types
    REFERABLE: set[function]

    def serializeBattle(battle: Battle) -> any:
        pass

    def deserializeBattle(serialized: str | any) -> Battle:
        pass

    pass
