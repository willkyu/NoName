class NON(object):
    def __init__(self) -> None:
        pass


class NONEntity(NON):
    def __init__(self, entity: NON) -> None:
        super().__init__()


class NONBattleEntity(NONEntity):
    def __init__(self, entity: NONEntity) -> None:
        super().__init__(entity)
