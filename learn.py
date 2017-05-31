#!/usr/bin/env python3
import argparse
import pickle
from game import Game
from game.players import QPlayer


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Initialize Q-data.',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('-o', '--outfile', type=str, default='qdata.p',
                        help='File to store the table of Q-values.')
    parser.add_argument('-i', '--iterations', type=int, default=200000,
                        help='Number of iterations to make for q-learning.')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Run program in debug mode.')
    args = parser.parse_args()

    player1 = QPlayer()
    player2 = QPlayer()
    g = Game(player1=player1, player2=player2)
    for i in range(args.iterations):
        if args.debug and (i + 1) % 100 == 0:
            print('{}/{}'.format(i + 1, args.iterations), end='\r')
        while not g.is_over():
            g.make_iteration()
        g.restart()
    print()
    with open(args.outfile, 'wb') as f:
        pickle.dump(g.Q_values, f)
