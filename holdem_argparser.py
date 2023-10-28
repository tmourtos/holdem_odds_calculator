import holdem_utils

from re import compile


class Args:
    """
        Wrapper class that holds the arguments for library calls
    """
    def __init__(self, board, hand_cards, num_sims):
        self.board = board
        self.cards = hand_cards
        self.num_sims = num_sims


def parse_args(args: Args):
    """
        Parse arguments passed to holdem_calculator as a library call
    :param args: The arguments passed to holdem_calculator
    :return: The hand cards and the board
    """
    validate_arguments(args)
    hand_cards, board = parse_cards(args.cards, args.board)
    return hand_cards, board, args.num_sims


def parse_cards(cards: list, board: list):
    """
        Parse hand cards and board
    :param cards: A list holding the player's cards
    :param board: A list holding the game board
    :return: The parsed player's hands and board
    """
    hand_cards = create_hand_cards(cards)
    if board:
        board = parse_board(board)
    return hand_cards, board


def validate_arguments(args: Args):
    """
        Validate the given arguments
    :param args: The arguments
    """
    if args.num_sims <= 0:
        print('Number of Monte Carlo simulations must be positive.')
        exit()
    all_cards = list(args.cards)
    if args.board:
        all_cards.extend(args.board)
    validate_cards(all_cards)


def validate_cards(all_cards: list):
    """
        Check that the hand cards + board are formatted properly and unique
    :param all_cards: The hand cards + board
    """
    card_re = compile('[AKQJT98765432][scdh]')
    for card in all_cards:
        if card != '?' and not card_re.match(card):
            print('Invalid card given.')
            exit()
        else:
            if all_cards.count(card) != 1 and card != '?':
                print('The cards given must be unique.')
                exit()


def create_hand_cards(raw_hand_cards: list) -> tuple:
    """
        Get hands in raw form and return tuple of two-tuple hand: e.g. ((As, Ks), (Ad, Kd), (Jh, Th))
    :param raw_hand_cards: The raw player's hand cards
    :return: The processed player's hand cards
    """
    if not raw_hand_cards or len(raw_hand_cards) < 2 or len(raw_hand_cards) % 2:
        print('You must provide a non-zero even number of hand cards')
        exit()

    hand_cards, current_hand_cards = list(), list()
    for hand_card in raw_hand_cards:
        if hand_card != "?":
            current_card = holdem_utils.Card(hand_card)
            current_hand_cards.append(current_card)
        else:
            current_hand_cards.append(None)
        if len(current_hand_cards) == 2:
            if None in current_hand_cards:
                if current_hand_cards[0] or current_hand_cards[1]:
                    print('Unknown hand cards must come in pairs')
                    exit()
            hand_cards.append((current_hand_cards[0], current_hand_cards[1]))
            current_hand_cards = list()
    if hand_cards.count((None, None)) > 1:
        print('Can only have one set of unknown hand cards')
    return tuple(hand_cards)


def parse_board(board: list):
    """
        Parse and validate board cards
    :param board: The board cards
    :return: The parsed and validated board cards
    """
    if len(board) > 5 or len(board) < 3:
        print('Board must have a length of 3, 4, or 5.')
        exit()
    if '?' in board:
        print('Board cannot have unknown cards')
        exit()
    return create_cards(board)


def create_cards(card_strings: list) -> list:
    """
        Instantiate new cards from the arguments and return them in a list
    :param card_strings: The card strings in list
    :return: The cards instances
    """
    return [holdem_utils.Card(arg) for arg in card_strings]
