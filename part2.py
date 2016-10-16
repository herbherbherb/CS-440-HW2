import numpy as np
import scipy as sp
from copy import copy, deepcopy

# class Node():

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

	white = []
	black = []
	matrix = []
##================Read_File===========================
	with open('breakthrough.txt') as f:
		content = f.readlines()
	content = [x.strip('\n') for x in content]
	for i in range(8):
		line = []
		for j in range(8):
			if content[i][j] == '1':
				piece = Piece(i, j, content[i][j])
				line.append(piece)
				black.append(piece)
			elif content[i][j] == '0':
				piece = Piece(i, j, content[i][j])
				line.append(piece)
				white.append(piece)
			else:
				line.append(None)
		matrix.append(line)

	print(matrix)

##===============================================

	white_player = True
	while True:
		node = Node(0, "white", matrix)
		best_node = minimax(node, 0, white, black, False)
		matrix = best_node.matrix
		if winner(matrix):
			if white_player:
				return matrix, "white"
			else:
				return matrix, "black"
		white_player = not white_player


def winner(matrix):
	return False


def minimax(node, white, black, is_offensive):
	if node.depth == 3:
		node.value = eval_func(is_offensive)
		return node

	if node.player == "white":
		node.children = next_moves(node, white)
	else:
		node.children = next_moves(node, black)

	best_node = None
	for child in node.children:
		cur_node = minimax(child, white, black, is_offensive)
		if not best_node:
			best_node = cur_node
		else:
			if node.depth == 0 or node.depth == 2:
				if best_node.value < cur_node.value:
					best_node = cur_node
			elif best_node.value > cur_node.value:
					best_node = cur_node
	return best_node

def next_moves(node, pieces):
	moves = []
	matrix = node.matrix
	for pawn in pieces:
		if pawn.captured:
			continue

		row = pawn.row
		col = pawn.col
		if player == "white":
			row -= 1
			if row < 0:
				continue
			next_loc = matrix[row][col]
			if not next_loc:
				new_matrix = matrix.copy()
				new_matrix[row][col] = new_matrix[row-1][col]
				new_matrix[row-1][col] = None
				moves.append(Node(node.depth+1, "black", new_matrix))
			new_col = col + 1
			if new_col <= 7:
				new_matrix = matrix.copy()
				next_loc = new_matrix[row][new_col]
				if not next_loc:
					new_matrix[row][new_col] = new_matrix[row-1][col]
					new_matrix[row-1][col] = None
					moves.append(Node(node.depth+1, "black", new_matrix))
				elif next_loc.player == "black":
					next_loc.captured = True
					next_loc.row = -1
					next_loc.col = -1

					new_matrix[row][new_col] = new_matrix[row-1][col]
					new_matrix[row-1][col] = None
					moves.append(Node(node.depth+1, "black", new_matrix))
			new_col = col - 1
			if new_col >= 0:
				new_matrix = matrix.copy()
				next_loc = new_matrix[row][new_col]
				if not next_loc:
					new_matrix[row][new_col] = new_matrix[row-1][col]
					new_matrix[row-1][col] = None
					moves.append(Node(node.depth+1, "black", new_matrix))
				elif next_loc.player == "black":
					next_loc.captured = True
					next_loc.row = -1
					next_loc.col = -1
					
					new_matrix[row][new_col] = new_matrix[row-1][col]
					new_matrix[row-1][col] = None
					moves.append(Node(node.depth+1, "black", new_matrix))

# def winning_
main()

