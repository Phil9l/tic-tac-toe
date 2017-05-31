import itertools
import numpy as np
from itertools import chain
from .data_types import FieldEntities, GameResult
from .exceptions import (NotEmptyFieldError, NoWinnerException)


__all__ = ['Field']


class Field:
    def __init__(self, size=3, win_length=3):
        self._size = size
        self._data = np.full((size, size), FieldEntities.EMPTY)
        self._win_length = win_length
        self._current_turn = FieldEntities.CROSS

    def __getitem__(self, key):
        if len(key) != 2:
            raise ValueError('2 arguments required')
        return self._data[key]

    def __str__(self):
        return str(self._data)

    @property
    def data(self):
        return self._data

    @property
    def empty_positions(self):
        return zip(*np.where(self._data == FieldEntities.EMPTY))

    @staticmethod
    def _get_winner_from_rows(*args, win_length):
        for row in chain(*args):
            for entity, group in itertools.groupby(row):
                if entity == FieldEntities.EMPTY:
                    continue
                if len(list(group)) >= win_length:
                    return entity
        raise NoWinnerException()

    @staticmethod
    def _next_turn(current_turn):
        data = {FieldEntities.CROSS: FieldEntities.NOUGHT,
                FieldEntities.NOUGHT: FieldEntities.CROSS}
        return data[current_turn]

    def copy(self):
        new_field = Field(self._size, self._win_length)
        new_field._data = np.copy(self._data)
        new_field._current_turn = self._current_turn
        return new_field

    def get_result(self):
        if np.all(self._data):
            return GameResult.DRAW
        try:
            winner = self.get_winner()
            return GameResult.CROSS_WIN if winner == FieldEntities.CROSS \
                else GameResult.NOUGHT_WIN
        except NoWinnerException:
            return GameResult.IN_PROGRESS

    def get_winner(self):
        rows = [i for i in chain(self._data, self._data.T)]
        diagonals = [self._data.diagonal(i)
                     for i in range(-self._size, self._size)]
        diagonals += [np.flipud(self._data).diagonal(i)
                      for i in range(-self._size, self._size)]
        return self._get_winner_from_rows(rows, diagonals,
                                          win_length=self._win_length)

    def is_over(self):
        if np.all(self._data):
            return True
        try:
            self.get_winner()
        except NoWinnerException:
            return False
        return True

    def put(self, x, y):
        if self._data[x, y] != FieldEntities.EMPTY:
            raise NotEmptyFieldError()
        self._data[x, y] = self._current_turn
        self._current_turn = self._next_turn(self._current_turn)
