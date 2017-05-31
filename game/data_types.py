import enum


class FieldEntities(enum.IntEnum):
    EMPTY = 0
    CROSS = 1
    NOUGHT = 2


class GameResult(enum.Enum):
    CROSS_WIN = 0
    NOUGHT_WIN = 1
    DRAW = 2
    IN_PROGRESS = 3