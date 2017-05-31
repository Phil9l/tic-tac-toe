from game.data_types import GameResult


DRAW_RESULT = 0.5
WIN_RESULT = 1.0
LOSE_RESULT = -1.0


def get_reward(field) -> float:
    if not field.is_over():
        return 0.0
    result = field.get_result()
    if result == GameResult.CROSS_WIN:
        return WIN_RESULT
    elif result == GameResult.NOUGHT_WIN:
        return LOSE_RESULT
    else:
        return DRAW_RESULT
