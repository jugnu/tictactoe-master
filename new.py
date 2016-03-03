
board = "- - - - - - - - -".split()
def nboard(board):
	temp = []
	newboard = []
	for x in xrange(0,9):
		if (x%3==0 and x!=0):
			newboard.append(temp)
			temp = [board[x]]
		else:
			temp.append(board[x])
	newboard.append(temp)
	return newboard

newBoard = board
print newBoard
n1 = newBoard
newBoard = {}
newBoard['board'] = n1
newBoard['moves'] = []
newBoard['utility'] = 0
newBoard['player'] = 'x'

def availMoves(board):
	temp = []
	currBoard = board['board']
	for x in xrange(0,3):
		for y in xrange(0,3):
#			print 'THIS:', board['board']
			if currBoard[x][y] == '-':
				temp.append((x,y))
	return temp

def evalUtility(board, player):
	currBoard = board['board']
	moves = []
	for x in xrange(0,3):
		for y in xrange(0,3):
			if currBoard[x][y] == player:
				moves.append((x,y))
	winmoves = [[(0,0),(0,1),(0,2)],[(1,0),(1,1),(1,2)],[(2,0),(2,1),(2,2)],[(0,0),(1,1),(2,2)],[(2,0),(1,1),(0,2)],[(1,0),(1,1),(1,2)],[(0,1),(1,1),(2,1)]]
	if moves in winmoves:
		if player == 'x':
			return 1
		else:
		 	return -1
	else:
		return 0
        return 0

newBoard['board'][1][2] = 'x'
newBoard['board'][1][1] = 'x'

def makeMove(board, move):
	if board['player'] == 'x':
		board['player'] = 'o'
	else:
		board['player'] = 'x'
	board['board'][move[0]][move[1]] = board['player']
	board['moves'].append(move)
	board['utility'] = evalUtility(board, board['player'])
	return board

def recurse(board, move):
	if move[0] != -1:
		board = makeMove(board, move)
	print board
	if board['utility'] == 0:
		newmoves = availMoves(board)
		for each in newmoves:
			board['utility'] = recurse(board, each)
	if board['utility'] == 1:
		if board['player'] == 'x':
			return 1
		else:
		 	return -1
	elif board['utility'] == -1:
	  	if board['player'] == 'x':
	  		return -1
	  	elif board['player'] == 'o':
	  		return 1
print 'play:', newBoard
recurse(newBoard, (2,2))
