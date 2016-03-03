#!/usr/bin/env python
'''Tic tac toe in python, Minimax with alpha-beta pruning.'''
import sys
import random
import getopt

# Board: array of 9 int, positionally numbered like this:
# 0  1  2
# 3  4  5
# 6  7  8

# Well-known board positions
WINNING_TRIADS = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7),
    (2, 5, 8), (0, 4, 8), (2, 4, 6))
PRINTING_TRIADS = ((0, 1, 2), (3, 4, 5), (6, 7, 8))
# The order in which slots get checked for absence of a player's token:
SLOTS = (0, 1, 2, 3, 4, 5, 6, 7, 8)

# Internal-use values.  Chosen so that the "winner" of a finished
# game has an appropriate value, as X minimizes and O maximizes
# the board's value (function board_valuation() defines "value")
# Internally, the computer always plays Os, even though the markers[]
# array can change based on -r command line flag.
X_token = -1
Open_token = 0
O_token = 1

# Strings for output: player's markers, phrase for end-of-game
MARKERS = ['_', 'O', 'X']
END_PHRASE = ('draw', 'win', 'loss')

HUMAN = 1
COMPUTER = 0

def board_valuation(board, player, next_player, alpha, beta):
    '''Dynamic and static evaluation of board position.'''
    # Static evaluation - value for next_player
    wnnr = winner(board)
    if wnnr != Open_token:
        # Not a draw or a move left: someone won
        return wnnr
    elif not legal_move_left(board):
        # Draw - no moves left
        return 0 # Cat
    # If flow-of-control gets here, no winner yet, not a draw.
    # Check all legal moves for "player"
    for move in SLOTS:
        if board[move] == Open_token:
            board[move] = player
            val = board_valuation(board, next_player, player, alpha, beta)
            board[move] = Open_token
            if player == O_token:  # Maximizing player
                if val > alpha:
                    alpha = val
                if alpha >= beta:
                    return beta
            else:  # X_token player, minimizing
                if val < beta:
                    beta = val
                if beta <= alpha:
                    return alpha
    if player == O_token:
        retval = alpha
    else:
        retval = beta
    return retval

def print_board(board):
    '''Print the board in human-readable format.
       Called with current board (array of 9 ints).
    '''
    for row in PRINTING_TRIADS:
        for hole in row:
            print MARKERS[board[hole]],
        print

def legal_move_left(board):
    ''' Returns True if a legal move remains, False if not. '''
    for slot in SLOTS:
        if board[slot] == Open_token:
            return True
    return False

def winner(board):
    ''' Returns -1 if X wins, 1 if O wins, 0 for a cat game,
        0 for an unfinished game.
        Returns the first "win" it finds, so check after each move.
        Note that clever choices of X_token, O_token, Open_token
        make this work better.
    '''
    for triad in WINNING_TRIADS:
        triad_sum = board[triad[0]] + board[triad[1]] + board[triad[2]]
        if triad_sum == 3 or triad_sum == -3:
            return board[triad[0]]  # Take advantage of "_token" values
    return 0

def determine_move(board):
    ''' Determine Os next move. Check that a legal move remains before calling.
        Randomly picks a single move from any group of moves with the same value.
    '''
    best_val = -2  # 1 less than min of O_token, X_token
    my_moves = []
    for move in SLOTS:
        if board[move] == Open_token:
            board[move] = O_token
            val = board_valuation(board, X_token, O_token, -2, 2)
            board[move] = Open_token
            print "My move", move, "causes a", END_PHRASE[val]
            if val > best_val:
                best_val = val
                my_moves = [move]
            if val == best_val:
                my_moves.append(move)
    return random.choice(my_moves)

def recv_human_move(board):
    ''' Encapsulate human's input reception and validation.
        Call with current board configuration. Returns
        an int of value 0..8, the Human's move.
    '''
    looping = True
    while looping:
        try:
            inp = input("Your move: ")
            yrmv = int(inp)
            if 0 <= yrmv <= 8:
                if board[yrmv] == Open_token:
                    looping = False
                else:
                    print "Spot already filled."
            else:
                print "Bad move, no donut."

        except EOFError:
            print
            sys.exit(0)
        except NameError:
            print "Not 0-9, try again."
        except SyntaxError:
            print "Not 0-9, try again."

        if looping:
            print_board(board)

    return yrmv

def usage(progname):
    '''Call with name of program, to explain its usage.'''
    print progname + ": Tic Tac Toe in python"
    print "Usage:", progname, "[-h] [-c] [-r] [-x] [-X]"
    print "Flags:"
    print "-x, -X:   print this usage message, then exit."
    print "-h:  human goes first (default)"
    print "-c:  computer goes first"
    print "-r:  computer is X, human is O"
    print "The computer O and the human plays X by default."

def main():
    '''Call without arguments from __main__ context.'''
    try:
        opts, args = getopt.getopt(sys.argv[1:], "chrxX",
            ["human", "computer", "help"])
    except getopt.GetoptError:
        # print help information and exit:
        usage(sys.argv[0])
        sys.exit(2)

    next_move = HUMAN # Human goes first by default

    for opt, arg in opts:
        if opt == "-h":
            next_move = HUMAN
        if opt == "-c":
            next_move = COMPUTER
        if opt == "-r":
            MARKERS[-1] = 'O'
            MARKERS[1] = 'X'
        if opt in ("-x", "-X", "--help"):
            usage(sys.argv[0])
            sys.exit(1)

    # Initial state of board: all open spots.
    board = [Open_token, Open_token, Open_token, Open_token, Open_token,
        Open_token, Open_token, Open_token, Open_token]

    # State machine to decide who goes next, and when the game ends.
    # This allows letting computer or human go first.
    while legal_move_left(board) and winner(board) == Open_token:
        print
        print_board(board)

        if next_move == HUMAN and legal_move_left(board):
            humanmv = recv_human_move(board)
            board[humanmv] = X_token
            next_move = COMPUTER

        if next_move == COMPUTER and legal_move_left(board):
            mymv = determine_move(board)
            print "I choose", mymv
            board[mymv] = O_token 
            next_move = HUMAN

    print_board(board)
    # Final board state/winner and congratulatory output.
    try:
        # "You won" should never appear on output: the program
        # should always at least draw.
        print ["Cat got the game", "I won", "You won"][winner(board)]
    except IndexError:
        print "Really bad error, winner is", winner(board)

    sys.exit(0)
#-------
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print
        sys.exit(1)
