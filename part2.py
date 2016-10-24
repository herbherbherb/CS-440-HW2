import numpy as np
from copy import copy, deepcopy
import time


class Node():
	def __init__(self, depth, player, matrix, value = 0):
		self.depth = depth
		self.player = player
		self.matrix = matrix
		self.value = value
		self.children = []

class Piece():
	def __init__(self, row, col, player):
		self.row = row
		self.col = col
		self.base = True if row == 0 or row == 7 else False
		self.captured = False
		self.player = player

	def __repr__(self):
		return self.player


def main():
	matrix = []
##================Read_File===========================
	with open('breakthrough.txt') as f:
		content = f.readlines()
	content = [x.strip('\n') for x in content]
	for i in range(8):
		line = []
		for j in range(8):
			if content[i][j] == '1':
				piece = Piece(i, j, 'black')
				line.append(piece)
			elif content[i][j] == '0':
				piece = Piece(i, j, 'white')
				line.append(piece)
			else:
				line.append(None)
		matrix.append(line)
##================Read_File===========================

	white_player = True
	player1_time = 0.
	player2_time = 0.
	player1_moves = 0
	player2_moves = 0
	player1_nodes = 0
	player2_nodes = 0

	best_node = None
	while True:
		color = "white"
		if not white_player:    		# find the color of current player
			color = "black"

		print_board(matrix)
		print()
		if winner(matrix):
			if white_player:
				player1_left, player2_left = count_left(matrix)
				print("White Player Win")
				print("Total Time for Player 1: ", player1_time)
				print("Total Time for Player 2: ", player2_time)
				print("Average Time for Player 1 per Turn: ", player1_time/player1_moves)
				print("Average Time for Player 2 per Turn: ", player2_time/player2_moves)
				print("Average Nodes Expanded by Player 1 per Turn: ", player1_nodes/player1_moves)
				print("Average Nodes Expanded by Player 2 per Turn: ", player2_nodes/player2_moves)
				print("White Player Captured: ", 16 - player2_left, " Opponent's Pieces")
				print("Black Player Captured: ", 16 - player1_left, " Opponent's Pieces")
				return matrix, "white"
			else:
				player1_left, player2_left = count_left(matrix)
				print("Black Player Win")
				print("Total Time for Player 1: ", player1_time, " Second")
				print("Total Time for Player 2: ", player2_time, " Second")
				print("Average Time for Player 1 per Turn: ", player1_time/player1_moves, " Second")
				print("Average Time for Player 2 per Turn: ", player2_time/player2_moves, "Second")
				print("Average Nodes Expanded by Player 1 per Turn: ", player1_nodes/player1_moves)
				print("Average Nodes Expanded by Player 2 per Turn: ", player2_nodes/player2_moves)
				print("White Player Captured: ", 16 - player2_left, " Opponent's Pieces")
				print("Black Player Captured: ", 16 - player1_left, " Opponent's Pieces")
				return matrix, "black"

		node = Node(0, color, matrix)
		#============================
		turn_time = 0
		if white_player:     				# white player always goes first     player 1
		# best_node, nodes_expanded = alphabeta(node, node, True, -np.inf, np.inf, 0)
			start_time = time.time()
			player1_moves += 1
			best_node, nodes_expanded = minimax(node, node, True, 0, 1)
			player1_nodes += nodes_expanded
			end = time.time()
			player1_time += end - start_time
			turn_time = end - start_time
		else:								# black player,     player 2
			start_time = time.time()
			player2_moves += 1
			best_node, nodes_expanded = minimax(node, node, True, 0, 1)
			player2_nodes += nodes_expanded
			end = time.time()
			player2_time += end - start_time
			turn_time = end - start_time
		#============================
		print("Max Possible Value: ", best_node.value)
		print("Nodes Expanded: ", nodes_expanded)
		print("Execution Time", turn_time)

		matrix = best_node.matrix
		white_player = not white_player

def count_left(matrix):
	player1 = player2 = 0
	for row in range(8):
		for col in range(8):
			if matrix[row][col] and matrix[row][col].player == 'white':
				player1 += 1
			elif matrix[row][col] and matrix[row][col].player == 'black':
				player2 += 1
	return player1, player2

def minimax(init_info, node, is_offensive, curr_node_expanded, max_depth): # goes to Depth 3
	if node.depth == max_depth:
		node.value = eval_func(init_info, node, is_offensive) # (initial state, stragety, current state)
		return node, 1

	if node.player == 'white': 
		node.children = next_moves(node, 'white')
	else:
		node.children = next_moves(node, 'black')

	best_node = None
	new_expansion = 0
	for child in node.children:
		cur_node, expansion = minimax(init_info, child, is_offensive, curr_node_expanded, max_depth) # best of the child nodes (world state)
		new_expansion += expansion
		# print(best_node, " ", cur_node)
		if node.depth == 0 and winner(child.matrix):
			return child, new_expansion
		if not best_node:
			if node.depth == 0:
				child.value = cur_node.value
				best_node = child
			else:
				best_node = cur_node
		else:
			if node.depth == 0 or node.depth == 2:  # max player's turn
				if best_node.value < cur_node.value: 
					if node.depth == 0:				# 
						child.value = cur_node.value
						best_node = child
					else:
						best_node = cur_node
			elif best_node.value > cur_node.value:  # min player's turn
				best_node = cur_node
	return best_node, new_expansion

def alphabeta(init_info, node, is_offensive, alpha, beta, curr_node_expanded):
	if node.depth == 5:
		node.value = eval_func(init_info, node, is_offensive) # (initial state, stragety, current state)
		return node, 1

	if node.player == 'white': 
		node.children = next_moves(node, 'white') #array of child nodes
	else:	
		node.children = next_moves(node, 'black') #array of child nodes

	best_node = None
	new_expansion = 0
	for child in node.children:
		cur_child, expansion = alphabeta(init_info, child, is_offensive, alpha, beta, curr_node_expanded)
		new_expansion += expansion
		if node.depth == 0 and winner(child.matrix):  
			return child, new_expansion
		if not best_node:			 			  # if best_node = None
			if node.depth == 0:
				child.value = cur_child.value
				best_node = child
			else:
				best_node = cur_child			
		else:
			if node.depth == 0 or node.depth == 2 or node.depth == 4: 	# if max player turn
				if (best_node.value < cur_child.value):
					if node.depth == 0:
						child.value = cur_child.value
						best_node = child
					else: 
						best_node = cur_child

				alpha = max(best_node.value, alpha)	# assign alpha to be max value in worst case
				if beta <= alpha:
					break;

			else:	# if min player turn
				if (best_node.value > cur_child.value):
					best_node = cur_child
					# beta = best_node.value
				beta = min(beta, best_node.value)
				if beta <= alpha:
					break;

	return best_node, new_expansion

def winner(matrix):
	for col in range(8):
		if (matrix[7][col] and matrix[7][col].player == 'black') or (matrix[0][col] and matrix[0][col].player == 'white'):
			return True

	black = False
	white = False
	for row in range(8):
		for col in range(8):
			piece = matrix[row][col]
			if piece:
				if piece.player == 'white':
					white = True
				else:
					black = True

			if black and white:
				return False
	
	return True

def eval_func(initial, cur, is_offensive):
	own_pieces_init = own_pieces_cur = 0
	opp_pieces_init = opp_pieces_cur = 0

	if winner(cur.matrix):
		return 200

	init_pos = 0
	cur_pos = 0
	if is_offensive:
		dist_vals = [1,2,3,4,6,8,10,200]
		for row in range(8):
			for col in range(8):
				#=========capture======================
				init_piece = initial.matrix[row][col]
				cur_piece = cur.matrix[row][col]
				if init_piece:
					if init_piece.player == initial.player:
						own_pieces_init += 1
					
						if initial.player == 'white':
							init_pos += dist_vals[7 - row]
						else:
							init_pos += dist_vals[row]
					else:
						opp_pieces_init += 1

				if cur_piece:
					if cur_piece.player == initial.player:
						own_pieces_cur += 1
					
						if initial.player == 'white':
							cur_pos += dist_vals[7 - row]
						else:
							cur_pos += dist_vals[row]
					else:
						opp_pieces_cur += 1

		score = (cur_pos - init_pos) + (opp_pieces_init - opp_pieces_cur) * 2 + (own_pieces_init - own_pieces_cur) * (-1)
	else:
		dist_vals = [1,1,2,3,4,5,6,200]
		for row in range(8):
			for col in range(8):
				#=========capture======================
				init_piece = initial.matrix[row][col]
				cur_piece = cur.matrix[row][col]
				if init_piece:
					if init_piece.player == initial.player:
						own_pieces_init += 1
					
						if initial.player == 'white':
							init_pos += dist_vals[7 - row]
						else:
							init_pos += dist_vals[row]
					else:
						opp_pieces_init += 1

				if cur_piece:
					if cur_piece.player == initial.player:
						own_pieces_cur += 1
					
						if initial.player == 'white':
							cur_pos += dist_vals[7 - row]
						else:
							cur_pos += dist_vals[row]
					else:
						opp_pieces_cur += 1

		score = (cur_pos - init_pos) + (opp_pieces_init - opp_pieces_cur) + (own_pieces_init - own_pieces_cur) * (-2)
	return score

def next_moves(node, piece_color): # generate all the possible moves for next state
	moves = []
	matrix = node.matrix      # current state

	for xrow in range(0,8):
		for xcol in range(0,8):
			pawn = node.matrix[xrow][xcol]
			if pawn and pawn.player == piece_color:
				row = pawn.row
				col = pawn.col
				if pawn.player == 'white':
					row -= 1
					if row < 0:
						continue
					moves.extend(helper2(row, col, matrix, node))
				else:
					row += 1
					if row > 7:
						continue
					moves.extend(helper2(row, col, matrix, node))
	return moves


def helper2(row, col, matrix, node):
	moves = []
	next_loc = matrix[row][col]
	if not next_loc:
		new_matrix = deepcopy(matrix)
		moves.extend(make_move(row, col, col, new_matrix, node))
	new_col = col + 1 		
	if new_col <= 7:
		moves.extend(move_helper(row, col, matrix, new_col, node))
	new_col = col - 1
	if new_col >= 0:
		moves.extend(move_helper(row, col, matrix, new_col, node))
	return moves


def move_helper(row, old_col, matrix, new_col, node):
	moves = []
	new_matrix = deepcopy(matrix)
	next_loc = new_matrix[row][new_col]
	color = "white"
	if node.player == "white":
		color = "black"

	if not next_loc:
		moves.extend(make_move(row, old_col, new_col, new_matrix, node))
	elif next_loc.player == color:
		next_loc.captured = True
		next_loc.row = -1
		next_loc.col = -1

		moves.extend(make_move(row, old_col, new_col, new_matrix, node))
	return moves


def make_move(row, old_col, new_col, new_matrix, node):
	moves = []
	color = "white"
	if node.player == "white":
		old_row = row + 1
		color = "black"
	else:
		old_row = row - 1

	# print(new_matrix, old_row, old_col, row, new_col)
	piece = new_matrix[old_row][old_col]
	piece.row = row
	piece.col = new_col
	new_matrix[row][new_col] = piece
	new_matrix[old_row][old_col] = None
	moves.append(Node(node.depth + 1, color, new_matrix))

	return moves

def print_board(matrix):
	for row in range(8):
		for col in range(8):
			loc = matrix[row][col]
			if loc:
				if loc.player == 'white':
					print('0', end='')
				else:
					print('1', end='')
			else:
				print('-',end='')
		print()


#=======================EXTRA_CREDIT================================

# def winning_
main()

