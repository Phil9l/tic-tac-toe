#!/usr/bin/env python3
import argparse
import pickle
from game import Game
from game.players import HumanPlayer, QPlayer


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Tic Tac Toe qlearning bot.',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('-i', '--infile', type=str, default='qdata.p',
                        help='Number of iterations to make for q-learning.')
    parser.add_argument('--player1', type=str, default='human',
                        help='First player type.',
                        choices=['human', 'qbot'])
    parser.add_argument('--player2', type=str, default='qbot',
                        help='Second player type.',
                        choices=['human', 'qbot'])
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Run program in debug mode.')
    args = parser.parse_args()

    player1, player2 = HumanPlayer(), HumanPlayer()
    if args.player1 == 'qbot':
        player1 = QPlayer(epsilon=0)
    if args.player2 == 'qbot':
        player2 = QPlayer(epsilon=0)

    if isinstance(player1, QPlayer) or isinstance(player2, QPlayer):
        with open(args.infile, 'rb') as f:
            q_values = pickle.load(f)
    else:
        q_values = None

    g = Game(player1=player1, player2=player2, Q_values=q_values)

    while not g.is_over():
        print(g.field)
        g.make_iteration()
    print(g.field)
