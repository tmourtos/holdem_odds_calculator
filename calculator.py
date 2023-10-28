import holdem_calculator
from time import time
from pprint import pprint


"""
Card Values
-----------
A: Ace
K: King
Q: Queen
J: Jack
T: Ten
9 8 7 6 5 4 3 2: Numbers

Card Suits
----------
s: Spades
c: Clovers
h: Hearts
d: Diamonds
"""

pocket_cards = ['As', 'Ts']
# board = ['Js', '3c', 'Qs']
board = list()

pocket_cards.extend(['?', '?'])


def main():
    hand_odds = holdem_calculator.calculate_odds(pocket_cards, board)
    pprint(hand_odds)


if __name__ == '__main__':
    start = time()
    main()
    print('Time elapsed: {} seconds'.format(round(time() - start, 3)))
