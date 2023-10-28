import multiprocessing
import holdem_argparser
import holdem_utils

NUM_SIMULATIONS = 200


def calculate_odds(pocket_cards: list, board: list):
    """
        Collect the arguments, create the deck and start the simulation
    :param pocket_cards: The players' hands (as list)
    :param board: The game board (as list)
    """
    args = holdem_argparser.Args(board, pocket_cards, NUM_SIMULATIONS)
    pocket_cards, board, num_sims = holdem_argparser.parse_args(args)
    deck = holdem_utils.generate_deck(pocket_cards, board)

    return run_simulation(pocket_cards, board, deck, num_sims)


def run_simulation(pocket_cards: tuple, given_board: tuple, deck: tuple, num_sims: int):
    """

    :param pocket_cards: The players' hands (as tuple)
    :param given_board: The game board (as tuple)
    :param deck: The game deck (as tuple
    :param num_sims: The number of simulation (for pocket hand strength)
    :return:
    """
    num_players = len(pocket_cards)
    board_length = 0 if given_board is None else len(given_board)
    print('Board: {}'.format(given_board))

    """
    Create data structures to manage multiple processes:
    
    1) winner_list: Number of times each player wins a hand
    2) result_probabilities: A list for each player holding the number of
        times each type of poker hand (e.g. flush, straight) occurred
    """
    num_processes = multiprocessing.cpu_count()
    num_poker_hands = len(holdem_utils.HAND_RANKINGS)
    num_histograms = num_processes * num_players * num_poker_hands

    winner_list = multiprocessing.Array('i', num_processes * (num_players + 1))
    result_probabilities = multiprocessing.Array('i', num_histograms)

    if given_board:
        generate_all_boards = holdem_utils.generate_exhaustive_boards
    else:
        generate_all_boards = holdem_utils.generate_random_boards

    if (None, None) in pocket_cards:
        pocket_cards = list(pocket_cards)
        unknown_index = pocket_cards.index((None, None))
        deck_list = list(deck)
        pool = multiprocessing.Pool(processes=num_processes,
                                    initializer=unknown_simulation_init,
                                    initargs=(pocket_cards, unknown_index,
                                              deck_list, generate_all_boards,
                                              board_length, given_board, num_sims,
                                              winner_list, result_probabilities))
        pool.map(unknown_simulation, holdem_utils.generate_pocket_cards(deck))
    else:
        find_winner(generate_all_boards, deck, pocket_cards, board_length,
                    given_board, num_sims, winner_list, result_probabilities)

    # Go through each parallel data structure and aggregate results
    combined_winner_list, combined_histograms = [0] * (num_players + 1), list()

    for _ in range(num_players):
        combined_histograms.append([0] * len(holdem_utils.HAND_RANKINGS))
    for index, element in enumerate(winner_list):
        combined_winner_list[index % (num_players + 1)] += element
    for index, element in enumerate(result_probabilities):
        combined_histograms[int((index / num_poker_hands) % num_players)][(index % num_poker_hands)] += element

    # holdem_utils.print_results(pocket_cards, combined_winner_list, combined_histograms)
    return holdem_utils.parse_result(pocket_cards, combined_winner_list, combined_histograms)


def unknown_simulation_init(pocket_cards_list, unknown_index, deck_list,
                            generate_all_boards, board_length, given_board, num_sims,
                            combined_winner_list, combined_result_histograms):
    """
        Initialize a simulation where opponent cards are unknown
    """
    unknown_simulation.pocket_cards_list = pocket_cards_list
    unknown_simulation.unknown_index = unknown_index
    unknown_simulation.deck = deck_list
    unknown_simulation.generate_all_boards = generate_all_boards
    unknown_simulation.board_length = board_length
    unknown_simulation.given_board = given_board
    unknown_simulation.num_sims = num_sims
    unknown_simulation.combined_winner_list = combined_winner_list
    unknown_simulation.combined_result_histograms = combined_result_histograms


def unknown_simulation(new_pocket_cards):
    """
        Simulation where opponent cards are unknown
    """
    # Extract parameters
    pocket_cards_list = unknown_simulation.pocket_cards_list
    unknown_index = unknown_simulation.unknown_index
    deck = unknown_simulation.deck[:]
    generate_all_boards = unknown_simulation.generate_all_boards
    board_length = unknown_simulation.board_length
    given_board = unknown_simulation.given_board
    num_sims = unknown_simulation.num_sims
    combined_winner_list = unknown_simulation.combined_winner_list
    combined_result_histograms = unknown_simulation.combined_result_histograms

    # Set simulation variables
    num_players = len(pocket_cards_list)
    result_histograms, winner_list = list(), [0] * (num_players + 1)
    for _ in range(num_players):
        result_histograms.append([0] * len(holdem_utils.HAND_RANKINGS))
    pocket_cards_list[unknown_index] = new_pocket_cards
    deck.remove(new_pocket_cards[0])
    deck.remove(new_pocket_cards[1])

    # Find winner
    holdem_utils.find_winner(generate_all_boards, deck, tuple(pocket_cards_list),
                             board_length, given_board, num_sims, winner_list,
                             result_histograms)

    # Write results to parallel data structure
    proc_name = multiprocessing.current_process().name
    proc_id = int(proc_name.split("-")[-1]) % multiprocessing.cpu_count()
    for index, result in enumerate(winner_list):
        combined_winner_list[proc_id * (num_players + 1) + index] += result
    for histogram_index, histogram in enumerate(result_histograms):
        for index, result in enumerate(histogram):
            combined_result_histograms[len(holdem_utils.HAND_RANKINGS) *
                                       (proc_id * num_players + histogram_index)
                                       + index] += result


def find_winner(generate_all_boards, deck, pocket_cards, board_length,
                given_board, num_sims, winner_list, result_probabilities):
    """
        Determine the simulation winner
    """
    num_processes = multiprocessing.cpu_count()
    # Create threadpool and use it to perform hand detection over all boards
    pool = multiprocessing.Pool(processes=num_processes,
                                initializer=simulation_init,
                                initargs=(given_board, pocket_cards, winner_list,
                                          result_probabilities))
    pool.map(simulation, generate_all_boards(deck, num_sims, board_length))


# Initialize shared variables for simulation
def simulation_init(given_board, pocket_cards, winner_list, result_probabilities):
    simulation.given_board = given_board
    simulation.pocket_cards = pocket_cards
    simulation.winner_list = winner_list
    simulation.result_probabilities = result_probabilities


# Separated function for each thread to execute while running
def simulation(remaining_board):
    # Extract variables shared through inheritance
    given_board, pocket_cards = simulation.given_board, simulation.pocket_cards
    winner_list = simulation.winner_list
    result_probabilities = simulation.result_probabilities

    # Generate a new board
    if given_board:
        board = given_board[:]
        board.extend(remaining_board)
    else:
        board = remaining_board
    num_players = len(pocket_cards)

    # Extract process id from the name of the current process
    # Names are of the format: PoolWorker-1 - PoolWorker-n
    proc_name = multiprocessing.current_process().name
    proc_id = int(proc_name.split("-")[-1]) % multiprocessing.cpu_count()

    # Create results data structure which tracks results of comparisons
    result_list = list()
    for _ in range(num_players):
        result_list.append(list())

    # Find the best possible poker hand given the created board and the
    # hole cards and save them in the results data structures
    suit_histogram, histogram, max_suit = (
        holdem_utils.preprocess_board(board))
    for index, hole_card in enumerate(pocket_cards):
        result_list[index] = (
            holdem_utils.detect_hand(hole_card, board, suit_histogram, histogram, max_suit))

    # Find the winner of the hand and tabulate results
    winner_index = holdem_utils.compare_hands(result_list)
    winner_list[proc_id * (num_players + 1) + winner_index] += 1

    # Increment what hand each player made
    for index, result in enumerate(result_list):
        result_probabilities[len(holdem_utils.HAND_RANKINGS) *
                          (proc_id * num_players + index) + result[0]] += 1
