import abc
import numpy as np
import random
from game.data_types import FieldEntities


class PlayerBase(metaclass=abc.ABCMeta):
    def __init__(self):
        self._game = None
        self._mark = None
        self._field = None

    @property
    def mark(self):
        return self._mark

    @abc.abstractmethod
    def get_move(self) -> (int, int):
        pass

    def set_mark(self, mark):
        self._mark = mark

    def set_game(self, game):
        self._game = game
        self._field = game.field


class HumanPlayer(PlayerBase):
    def get_move(self):
        return list(map(int, input('Enter your position(e.g. 0 0): ').split()))


class RandomPlayer(PlayerBase):
    def get_move(self):
        moves = list(self._game.field.empty_positions)
        if moves:
            return random.choice(moves)


class QPlayer(PlayerBase):
    def __init__(self, Q_values=None, epsilon=0.9):
        super().__init__()
        self._Q_values = {} if Q_values is None else Q_values
        self._epsilon = epsilon

    def get_move(self):
        if len(self._Q_values) == 0 or random.random() < self._epsilon:
            player = RandomPlayer()
            player.set_mark(self._mark)
            player.set_game(self._game)
            return player.get_move()

        state_key = QPlayer.make_Q_values(self._field, self._mark,
                                          self._Q_values)
        Q_values = self._Q_values[state_key]

        if self._mark == FieldEntities.CROSS:
            return QPlayer.stochastic_argminmax(Q_values, max)
        elif self._mark == FieldEntities.NOUGHT:
            return QPlayer.stochastic_argminmax(Q_values, min)

    @classmethod
    def make_Q_values(cls, field, mark, Q_values):
        default_Qvalue = 1.0
        state_key = cls.get_state(field, mark)
        if state_key not in Q_values:
            moves = field.empty_positions
            Q_values[state_key] = {move: default_Qvalue for move in moves}
        return state_key

    @staticmethod
    def get_state(field, mark):
        return tuple(field.data.flatten()) + (mark.name,)

    @staticmethod
    def stochastic_argminmax(Q_values, func):
        best_Q_value = func(Q_values.values())
        if list(Q_values.values()).count(best_Q_value) > 1:
            best_options = [move for move in Q_values
                            if Q_values[move] == best_Q_value]
            move = random.choice(best_options)
        else:
            move = func(Q_values, key=Q_values.get)
        return move

    def update_Q_values(self, new_values):
        self._Q_values = new_values
