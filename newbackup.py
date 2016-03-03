board = "- - - - - - - - -".split()
import sys
import random
import getopt

moves = (0,1,2,3,4,5,6,7,8)
X_token = -1
Open_token = 0
O_token = 1
rtokens = {-1: 'X', 0: '-', 1:'O'}
tokens = {'X': -1, 'O': 1, '-': 0}
MARKERS = ['-', 'O', 'X']
END_PHRASE = ('draw', 'win', 'loss')

HUMAN = 1
COMPUTER = 0

##
WINPOS = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))

def winner(board):
	for each in WINPOS:
		sum = tokens[board[each[0]]]+tokens[board[each[1]]]+tokens[board[each[2]]]
		if sum == 3 or sum == -3:
			return tokens[board[each[0]]]
	return 0

def availMoves(board):
	temp = []
	currBoard = board['board']
	for x in xrange(0,3):
		for y in xrange(0,3):
#			print 'THIS:', board['board']
			if currBoard[x][y] == '-':
				temp.append((x,y))
	return temp

CAUSES = ('draw', 'win', 'loss')
def move_left(board):
	for each in moves:
		if board[each] == '-':
			return True
	return False
board[0] = 'X'
board[2] = 'O'
board[4] = 'X'
def minmax(board, player, next_player, alpha, beta):
	winnr = winner(board)
	if winnr!=Open_token:
		return winnr
	elif not move_left(board):
		return 0
	for move in moves:
		if board[move] == rtokens[Open_token]:
			board[move] = rtokens[player]
			val = minmax(board, next_player, player, alpha, beta)
			board[move] = rtokens[Open_token]
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
			
def determine(board):
	best_val = -2
	my_moves = []
	for move in moves:
		if board[move] == rtokens[Open_token]:
			board[move] = rtokens[O_token]
			val = minmax(board, X_token, O_token, -2, 2)
			board[move] = rtokens[Open_token]
			print move, ' causes ', CAUSES[val]
			if val> best_val:
				best_val = val
				my_moves = [move]
			elif val == best_val:
				my_moves.append(move)
	return random.choice(my_moves)
print board
final = determine(board)
print "I pick ", final
