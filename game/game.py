import contextlib
import qlearning.utils
from .field import Field, GameResult, FieldEntities
from .players import HumanPlayer, QPlayer
from .exceptions import NoWinnerException, NotEmptyFieldError


class Game:
    def __init__(self, player1=None, player2=None, *, size=3, win_length=3,
                 Q_values=None):
        self._player_index = 0
        self._size, self._win_length = size, win_length
        self._field = Field(size, win_length)
        self._Q_values = {} if Q_values is None else Q_values

        if player1 is None:
            player1 = HumanPlayer()
        if player2 is None:
            player2 = HumanPlayer()

        player1.set_mark(FieldEntities.CROSS)
        player2.set_mark(FieldEntities.NOUGHT)

        self._players = (player1, player2)

        for player in self._players:
            player.set_game(self)

        self.share_Q_values()

        self.gamma = 0.9
        self.alpha = 0.3

    @property
    def current_player(self):
        return self._players[self._player_index]

    @property
    def next_player(self):
        return self._players[(self._player_index + 1) % 2]

    @property
    def field(self):
        return self._field

    @property
    def Qlearning(self):
        return any(isinstance(player, QPlayer) for player in self._players)

    @property
    def Q_values(self):
        return self._Q_values

    @staticmethod
    def get_new_field(field, move):
        new_field = field.copy()
        new_field.put(*move)
        return new_field

    def get_result(self):
        return self._field.get_result()

    def get_winner(self):
        return self._field.get_winner()

    def is_over(self):
        return self._field.get_result() != GameResult.IN_PROGRESS

    def make_iteration(self):
        with contextlib.suppress(NotEmptyFieldError):
            move = tuple(self.current_player.get_move())
            if self.Qlearning:
                self.update_Q_values(move)
            self._field.put(*move)
            self._player_index = (self._player_index + 1) % 2

    def restart(self):
        self._field = Field(self._size, self._win_length)
        self._player_index = 0

    def share_Q_values(self):
        for player in self._players:
            if isinstance(player, QPlayer):
                player.update_Q_values(self._Q_values)

    def update_Q_values(self, move):
        state_key = QPlayer.make_Q_values(self.field, self.current_player.mark,
                                          self._Q_values)

        next_field = self.get_new_field(self._field, move)
        reward = qlearning.utils.get_reward(next_field)

        next_state_key = QPlayer.make_Q_values(next_field,
                                               self.next_player.mark,
                                               self._Q_values)
        if next_field.is_over():
            expected = reward
        else:
            next_Q_values = self._Q_values[next_state_key]
            expected = 0
            if self.current_player.mark == FieldEntities.CROSS:
                expected = reward + (self.gamma * min(next_Q_values.values()))
                # print('QVALUES:', next_Q_values.values())
            elif self.current_player.mark == FieldEntities.NOUGHT:
                expected = reward + (self.gamma * max(next_Q_values.values()))
                # print('QVALUES:', next_Q_values.values())
        difference = self.alpha * (expected - self._Q_values[state_key][move])
        # print(reward, expected, difference)
        self._Q_values[state_key][move] += difference
