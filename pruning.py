board = [['o', 'o', 'o','x', 'o','x', 'o','x', 'o'],
      ['o', 'o', '-','x', '-','x', 'o','x', 'o'],
      ['o', '-', 'o','x', '-','x', 'o','x', 'x'],
      ['o', 'o', '-','x', '-','x', 'x','x', '-'],
      ['o', 'o', '-','x', '-','x', 'o','x', 'o'],
      ['-', 'o', 'o','x', '-','x', 'o','x', 'o'],
      ['o', 'o', '-','x', '-','x', 'o','x', 'o'],
      ['o', 'o', '-','x', '-','x', 'o','x', 'o'],
      ['o', 'o', '-','x', '-','x', 'o','x', 'o']
      ]
#board = [['-', 'x', '-', 'x', 'x', 'o', 'o', '-', 'o'], ['o', 'x', 'x', 'x', 'o', 'x', '-', 'x', 'x'], ['o', 'x', 'o', 'x', 'x', 'o', 'x', '-', 'o'], ['x', 'o', 'x', 'o', 'x', 'x', 'o', 'o', 'o'], ['o', 'o', 'o', 'x', 'x', 'o', 'x', 'o', 'x'], ['o', 'x', 'o', 'o', 'x', 'x', 'x', 'x', 'x'], ['x', 'x', 'x', 'o', 'o', 'o', 'x', '-', 'o'], ['o', '-', '-', 'x', 'o', 'o', '-', 'x', '-'], ['o', 'x', '-', 'o', 'o', 'o', 'o', 'x', '-']]
import sys
import random

moves = (0,1,2,3,4,5,6,7,8)
X_token = -1
Open_token = 0
O_token = 1
rtokens = {-1: 'x', 0: '-', 1:'o'}
tokens = {'x': -1, 'o': 1, '-': 0}
MARKERS = ['-', 'o', 'x']
END_PHRASE = ('draw', 'win', 'loss')

HUMAN = 1
COMPUTER = 0

##
WINPOS = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
final_board={0:{},1:{},2:{},3:{},4:{},5:{},6:{},7:{},8:{}}

#board = [1, 1, 1,-1, 1,-1, 1,-1, 1,
#        1, 1, 0,-1, 0,-1, 1,-1, 1,
#	 1, 0, 1,-1, 0,-1, 1,-1, -1,
#	 1, 1, 0,-1, 0,-1, -1,-1, 0,
#	 1, 1, 0,-1, 0,-1, 1,-1, 1,
#	 0, 1, 1,-1, 0,-1, 1,-1, 1,
#	 1, 1, 0,-1, 0,-1, 1,-1, 1,
#	 1, 1, 0,-1, 0,-1, 1,-1, 1,
#	 1, 1, 0,-1, 0,-1, 1,-1, 1,
#	 ]
#Json Schema for the structure for the final_board
#final_board = {
#               0(This represents the small board number) : { 0:'',1:'',2:''......8:'',win:('o' for o and 'x' for x and '-' for none)  This contains the info about that small board}
#		}
#An example for the above json schema
#final_board = { 0:{1:'x',2:'o',3:'-',4:'x',5:'-',6:'x',7:'-',8:'-','win':'-'}}

def winner(board):
	for each in WINPOS:
		sum = tokens[final_board[each[0]]['win']]+tokens[final_board[each[1]]['win']]+tokens[board[each[2]]['win']]
		if sum == 3 or sum == -3:
			return tokens[board[each[0]]]
	return 0
def config_win(small_config):
    for each in WINPOS:
	sum = tokens[small_config[each[0]]] + tokens[small_config[each[1]]] + tokens[small_config[each[2]]]
	if sum == 3:
	    small_config['win'] = 'o'
	    return 
	if sum == -3:
	    small_config['win'] = 'x'
	    return 
	else:
	    small_config['win'] = '-'

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
small_board = 0;

def evaluate(final_board,player):
        for each in WINPOS:
	         if(final_board[each[0]]['win'] == rtokens[player]):
			 sum = 1;
		 if(final_board[each[1]]['win'] == rtokens[player]):
			 sum += 1;
		 if(final_board[each[2]]['win'] == rtokens[player]):
			 sum += 1;
	         if((final_board[each[1]]['win'] != rtokens[player]) or (final_board[each[0]]['win'] != rtokens[player]) or (final_board[each[2]]['win'] != rtokens[player])):
			 sum = 0; #As their is no chance of winning in this position
                 if(final_board[each[0]]['win'] == rtokens[next_player]):
			 sum -= 1;
	         if(final_board[each[1]]['win'] == rtokens[next_player]):
			 sum -= 1;
		 if(final_board[each[2]]['win'] == rtokens[next_player]):
			 sum -= 1;
	if(sum>0):
		heuristic = 1000*pow(10,sum)
	elif (sum<0):
		sum = -sum;
		heuristic = -1000*pow(10,sum)
	else:
		heuristic = 1
	return heuristic



def minmax(board,small_board,player, next_player, alpha, beta,depth):
	winnr = winner(final_board)
	if winnr!=Open_token:
		return winnr
	elif not move_left(final_board):
		return 0
	if small_board!=10:
	    for move in moves:
		if final_board[small_board][move] == rtokens[Open_token]:
			final_board[small_board][move] = rtokens[player]
 		        if(depth==4):
#				val = evaluate(final_board,player,next_player)
				val = 1
				return val
		        else:
			        val = minmax(final_board,move,next_player, player, alpha, beta,depth+1)
			        final_board[small_board][move] = rtokens[Open_token]
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
def choose_board(final_board):   #This function will contain the intelligence for choosing the small board in case of free choice
	for small_board in final_board:
	        if (final_board[small_board]['win']!='-'):
			continue;
		for i in final_board[small_board]:
		        if (final_board[small_board][i]=='-'):
				small_boards.append(small_board)
	return small_boards

def determine(final_board,small_board):
        if (small_board == 0):
                small_boards = [0,1,3] 
	elif (small_board == 2):
                small_boards = [1,2,5]
	elif (small_board == 6):
                small_boards = [3,6,7]
	elif (small_board == 8):
                small_boards  = [7,8,5]
	else:
	        small_boards = [small_board]
        print small_boards
        if (len(small_boards) > 0):
                for i in small_boards:
                        if(final_board[i]['win']!='-'):
				small_boards.remove(i)
        print small_boards
	if (len(small_boards)==0):
		small_boards = choose_board(final_board)
	best = -2
	for small_board in small_boards:
		temp = ret_val(final_board,small_board)
		if temp[0]>best:
			best = temp[0]
	                my_moves = [temp[1]]

	return my_moves[0]


def ret_val(final_board,small_board):
	best_val = -2;
	print "begin again!"
	my_moves = []
	for move in moves:
	        if final_board[small_board][move] == rtokens[Open_token]:
		        print "i am here"
			print move
			final_board[small_board][move] = rtokens[O_token]
			val = minmax(final_board,small_board,X_token,O_token,-2,2,0)
			print "Val: ", val
			print final_board[small_board]
			print move
	                final_board[small_board][move] = rtokens[Open_token]
			if val > best_val:
			        best_val= val
			        my_moves = [(small_board,move)]
			elif val == best_val:
				my_moves.append((small_board, move))
	print "My moves: ", my_moves
	return (best_val,my_moves[0])

i = 0
j = 0
for x in board:
	for y in x:
		final_board[i][j] = y
		j = j+1
		if(j == 9):
			config_win(final_board[i])
	i = i+1
	if (i == 9):
		break
	j = j % 9
print  final_board
final = determine(final_board,0)
print "I pick ", final
