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
FIRST_FLAG = 0
small_board = 0;
CAUSES = ('draw', 'win', 'loss')

class Player75:
	
	def __init__(self):
		pass


	def winner(self, final_board,player,next_player):
		for each in WINPOS:
			sum = 0
			win_check = {rtokens[player]: 1, rtokens[next_player]: -1, '-': 0}
			sum = win_check[final_board[each[0]]['win']] + win_check[final_board[each[1]]['win']] + win_check[final_board[each[2]]['win']]
			if sum == 3:
			        return 100000
			elif sum == -3: 
			        return -100000
		return 0

	def config_win(self, small_config):
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

	def eval_small(self, small_board,player,next_player):
		sum = 0
		oppo_sum = 0
		heuristic = 0
		global WINPOS
		for each in WINPOS:
			sum = 0
			oppo_sum = 0
		        for i in each:
		            if(small_board[i] == rtokens[player]):
				    sum += 1
		            elif(small_board[i] == rtokens[next_player]):
	                            oppo_sum += 1
			if(sum > 0):
		        	heuristic = heuristic + (pow(10,sum))
			if(oppo_sum > 0):
		        	heuristic = heuristic - (pow(10,oppo_sum))
		return heuristic

	def evaluate(self, final_board,player,next_player):
		global WINPOS
		heuristic = 0
	        for each in WINPOS:
			 sum = 0
		         oppo_sum = 0
		         if(final_board[each[0]]['win'] == rtokens[player]):
				 sum += 1;
			 if(final_board[each[1]]['win'] == rtokens[player]):
				 sum += 1;
			 if(final_board[each[2]]['win'] == rtokens[player]):
				 sum += 1;
	                 if(final_board[each[0]]['win'] == rtokens[next_player]):
				 oppo_sum -= 1;
		         if(final_board[each[1]]['win'] == rtokens[next_player]):
				 oppo_sum -= 1;
			 if(final_board[each[2]]['win'] == rtokens[next_player]):
				 oppo_sum -= 1;
			 if(sum>0):
			 	heuristic = heuristic + 100*pow(10,sum)
			 if(oppo_sum < 0):
			 	heuristic = heuristic - 100*pow(10,-oppo_sum)
		for small_board in final_board:
		        heuristic = heuristic + self.eval_small(final_board[small_board], player, next_player)
		return heuristic


	def valid_moves(self, final_board,last_move):
	   	small_board = last_move[1]
		if (small_board == -1):
			small_boards = [0,1,2,3,4,5,6,7,8]
		elif(small_board == 0):
			small_boards = [0,1,3]
		elif (small_board == 2):
			small_boards = [1,2,5]
		elif (small_board == 6):
			small_boards = [3,6,7]
		elif (small_board == 8):
			small_boards  = [7,8,5]
		else:
			small_boards = [small_board]
	 
		if (len(small_boards) > 0):
			temp_small_board = small_boards[:]
			for i in small_boards:
				if(final_board[i]['win']!=rtokens[Open_token]):
					temp_small_board.remove(i)
			small_boards = temp_small_board[:]
		if (len(small_boards)==0):
			small_boards = self.choose_board(final_board)
		valid_moves = []
		for small_board in small_boards:
	 		for i in final_board[small_board]:
				if i!='win' and final_board[small_board][i] == rtokens[Open_token]:
					valid_moves.append((small_board,i))
	 	return valid_moves

	def minmax(self, final_board,player, next_player, alpha, beta,depth,last_move, FINAL_DEPTH):
		winnr = self.winner(final_board,next_player,player)
		if winnr!=Open_token:
			return winnr*100
		moves = []
		moves = self.valid_moves(final_board,last_move)
		if 1:
			for move in moves:
				if final_board[move[0]][move[1]] == rtokens[Open_token]:
			                temp_dict = {}
					for i in final_board:
					        temp_dict[i] = final_board[i]
					final_board[move[0]][move[1]] = rtokens[player]
					for i in final_board:
						self.config_win(final_board[i])
					i = 0
					if(depth==FINAL_DEPTH):
						if(depth%2 != 0):
							val = self.evaluate(final_board,next_player,player)
						else:
							val = self.evaluate(final_board,player,next_player)
					else:
						val = self.minmax(final_board,next_player, player, alpha, beta,depth+1,move, FINAL_DEPTH)
					final_board[move[0]][move[1]] = rtokens[Open_token]
					for i in final_board:
						self.config_win(final_board[i])
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
					final_board = temp_dict
			if player == O_token:
				retval = alpha
			else:
				retval = beta
		return retval

	def choose_board(self, final_board):   #This function will contain the intelligence for choosing the small board in case of free choice
		small_boards = []
		for small_board in final_board:
		        if (final_board[small_board]['win']==rtokens[Open_token]):
				for i in xrange(0,9):
					if (final_board[small_board][i]==rtokens[Open_token]):
						small_boards.append(small_board)
						break
		return small_boards

	def determine(self, final_board,small_board):
		my_moves = []
		if (small_board == -1):
			small_boards = [0,1,2,3,4,5,6,7,8]
		elif(small_board == 0):
			small_boards = [0,1,3]
		elif (small_board == 2):
			small_boards = [1,2,5]
		elif (small_board == 6):
			small_boards = [3,6,7]
		elif (small_board == 8):
			small_boards  = [7,8,5]
		else:
			small_boards = [small_board]
		temp_small_board = small_boards[:]
		if (len(small_boards) > 0):
			for i in small_boards:
				if(final_board[i]['win']!=rtokens[Open_token]):
					temp_small_board.remove(i)
		small_boards = temp_small_board[:]
		temp_list = []

		if (len(small_boards) > 0):
			for small_board in small_boards:
				for i in xrange(0,9):
					if(final_board[small_board][i] == rtokens[Open_token]):
						temp_list.append(small_board)
						break
		small_boards = temp_list
		if (len(small_boards)==0):
			small_boards = self.choose_board(final_board)
		best = -10000000
		temp_dict = {}
		for small_board in small_boards:
		        temp_dict = {}
			for i in final_board:
			        temp_dict[i] = final_board[i]
			if len(small_boards)>5:
				temp = self.ret_val(final_board,small_board, 2)
			else:
				temp = self.ret_val(final_board, small_board, 3)
			if temp[0]>best:
				best = temp[0]
				my_moves = [temp[1]]
			final_board = temp_dict
		return my_moves[0]


	def ret_val(self, final_board,small_board, depth):
		best_val = -1000000;

		my_moves = []
		temp_dict = {}
		for i in final_board:
		        temp_dict.update({i:final_board[i]})
		moves = [0,1,2,3,4,5,6,7,8]
		for move in moves:
			if final_board[small_board][move] == rtokens[Open_token] and final_board[small_board]['win'] == rtokens[Open_token]:
			        for i in final_board:
				        self.config_win(final_board[i])
				final_board[small_board][move] = rtokens[O_token]
				val = self.minmax(final_board,-O_token,+O_token,-1000000,1000000, 1,(small_board,move), depth)
				final_board[small_board][move] = rtokens[Open_token]
				for i in final_board:
					self.config_win(final_board[i])

				if val > best_val:
					best_val= val
					my_moves = [(small_board,move)]
				elif val == best_val:
					my_moves.append((small_board, move))
	         
				final_board = temp_dict
		return (best_val,my_moves[random.randrange(len(my_moves))])

	def move(self,temp_board,temp_block,old_move,flag):
		i = 0
		j = 0
		count = 0
		global final_board
		global FIRST_FLAG
		if FIRST_FLAG == 0:
			for x in xrange(0,9):
				for y in xrange(0,9):
					m = 3*(x/3) + (y/3)
					n = 3*(x%3) + (y%3)
					final_board[m][n] = temp_board[x][y]
					if (final_board[m][n] != '-'):
						count = count + 1
			FIRST_FLAG = 1
		else:
			m = 3*(old_move[0]/3) + (old_move[1]/3)
			n = 3*(old_move[0]%3) + (old_move[1]%3)
			if flag == 'x':
				final_board[m][n] = 'o'
			else:
				final_board[m][n] = 'x'
		for i in final_board:
			self.config_win(final_board[i])
		global O_token, X_token
		if flag == 'x':
			O_token = -1
			X_token = 1
		else:
			O_token = 1
			X_token = -1
		if(old_move == (-1,-1)):
			final_board[4][4] = flag
			return (4,4)
	    	x = old_move[1]
		y = old_move[0]
		small_board = 3*(y%3) + (x%3)
		temp_dict = {}
		for i in final_board:
		        temp_dict.update({i:final_board[i]})
	  	final = self.determine(final_board,small_board)
	  	final_board = temp_dict
	        x = final[0]
	        y = final[1]
	        final_board[x][y] = flag
	        row = 3*(x/3) + (y/3)
	        column = 3*(x%3) + (y%3)
		return (row,column)