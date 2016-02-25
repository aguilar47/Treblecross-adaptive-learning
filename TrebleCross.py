__author__ = 'Aguilar'

from collections import defaultdict
import random
random.seed()


class MatchBox:
    # A matchbox consists of the game_board configuration,
    # the possible moves for this game_board, and the initial
    # one point (or poker chips) for each move.
    def __init__(self, game_board):
        self.board = game_board[:]

        # key: move index, value: points for this move
        self.possible_moves = {}

        # assign the points for each move
        for i, j in enumerate(self.board):
            if not j:
                self.possible_moves[i] = 1


class GameData:
    def __init__(self):
        self.score_sheet = []
        self.wins = 0
        self.boards = []
        self.matchboxes = {}
        self.last_move_index = []
        self.move_index = []
        self.resigns = 0


comp1_data = GameData()
comp2_data = GameData()


def treble_cross():
    num_of_squares = 0
    games_played = 0

    while num_of_squares < 3:
        # number of boxes that you want to play with
        num_of_squares = int(input("How many Boxes do you want to play with? "))
        if num_of_squares >= 3:
            break
        print("\nYou need at least 3 boxes to play.\n")

    games_to_play = int(input("How many games do you want the computers to play? "))

    while games_played < games_to_play:
        # initialize the game_board
        game_board = [False for _ in range(num_of_squares)]
        # start playing
        play(game_board)
        games_played += 1

    print("\n\n***COMPUTER 1 RESULTS***")
    print("Wins: {0}".format(comp1_data.wins))
    print("Resigns: {0}".format(comp1_data.resigns))

    print("\n\n***COMPUTER 2 RESULTS***")
    print("Wins: {0}".format(comp2_data.wins))
    print("Resigns: {0}".format(comp2_data.resigns))


def play(game_board):

    game_over = False
    # keep track of the number of moves made
    moves = 0

    while not game_over:

        # comp1 move
        moves, resign = make_move(game_board, comp1_data, moves)

        if resign:
            handle_resign(resigner=comp1_data, winner=comp2_data)
            break
        # check to see if the computer won.
        # if more than three moves have been made
        # then check if anybody has won
        if moves >= 3:
            game_over = check_for_win(game_board)
            if game_over:
                handle_end_game(winner=comp1_data, loser=comp2_data)
                break

        # comp2 move
        moves, resign = make_move(game_board, comp2_data, moves)
        if resign:
            handle_resign(resigner=comp2_data, winner=comp1_data)
            break

        # check to see if the computer won.
        # if more than three moves have been made
        # then check if anybody has won
        if moves >= 3:
            game_over = check_for_win(game_board)
            if game_over:
                handle_end_game(winner=comp2_data, loser=comp1_data)
                break


def make_move(game_board, comp_data, moves):
    if str(game_board) not in comp_data.matchboxes:
        # create the matchbox if it doesnt exist
        matchbox = MatchBox(game_board)
        comp_data.matchboxes[str(game_board)] = matchbox

    move_position, comp_data.last_move_index, resign = calculate_move(game_board, comp_data.matchboxes)

    if resign:
        return moves + 1, resign

    comp_data.move_index.append(comp_data.last_move_index)
    if game_board[move_position] is False:
        game_board[move_position] = True
    else:
        raise Exception('Move cannot be made. ')

    return moves + 1, False


def handle_end_game(*, winner, loser):
    loser.score_sheet.append("L")
    winner.score_sheet.append("W")
    winner.wins += 1

    loser.matchboxes = punish_move(loser.matchboxes, loser.move_index)


def handle_resign(*, resigner, winner):
    resigner.resigns += 1
    handle_end_game(winner=winner, loser=resigner)


# simply prints the board to the console
def print_board(game_board):
    sb = ["| "]
    for i, move in enumerate(game_board,  1):
        if move:
            sb.append("X")
        else:
            sb.append("{0}".format(i))
        sb.append(" | ")
    print(''.join(sb))


def check_for_win(game_board):
    # a win consists of three X's in a row.
    # We are using True as an X instead.
    game_over = False
    for i in range(len(game_board) - 2):
        if game_board[i] and game_board[i + 1] and game_board[i + 2]:
            game_over = True
    return game_over


def calculate_move(game_board, matchboxes):
    resign = False
    index = None
    matchbox = matchboxes.get(str(game_board))
    possible_moves = matchbox.possible_moves
    chips = [possible_moves[k] for k in possible_moves]
    chip_sum = sum(chips)

    if chip_sum <= 0:
        return 0, [game_board[:], 0], True

    r = random.randint(1, chip_sum)
    # randomly select a moved and take the weigths
    # into consideration.
    while r > 0:
        for i in possible_moves:
            index = i
            r -= possible_moves[i]
            if r < 1:
                break

    move = index
    last_move_index = (game_board[:], index)
    return move, last_move_index, resign


# update the matchbox for the loser.
def punish_move(matchboxes, move_index):
    # if the last move index is 0 then punish the move before that, otherwise
    # punish the last one

    game_board = move_index[-1][0]
    matchbox = matchboxes.get(str(game_board))
    chip_sum = sum(matchbox.possible_moves.values())

    if chip_sum == 0:
        move_before_last = move_index[-2][1]
        game_board = move_index[-2][0]
        matchbox = matchboxes.get(str(game_board))
        matchbox.possible_moves[move_before_last] -= 1
    else:
        # punish this move
        last_move = move_index[-1][1]
        matchbox.possible_moves[last_move] -= 1

    return matchboxes


treble_cross()


