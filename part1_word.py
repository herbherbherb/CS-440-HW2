import numpy as np
from copy import copy, deepcopy
import time

class Constraint():
	def __init__(self, word):
		self.word = word
		self.index = 0
		self.orient = None
		self.start = (-1,-1)
		self.done = False


count = 0

def main():
	matrix = []
##================Read_File===========================
	with open('sudoku') as f:
		content = f.readlines()
	content = [x.strip('\n') for x in content]
	
	for i in range(9):
		line = []
		for j in range(9):
			line.append(content[i][j])
		matrix.append(line)

	with open('bank1.txt') as f:
		content = f.readlines()
	content = [x.strip('\n') for x in content]
	content.sort(key = lambda s: len(s), reverse = True)
	print(content)
	word_bank = []
	for word in content:
		word_bank.append(Constraint(word.upper()))


	# # l = []
	# # for word in word_bank:
	# # 	l.extend(fit(matrix, word, 6, 8))
	start_time = time.time()
	solution, words, nodes_expanded = solve(matrix, word_bank, 0)
	end = time.time()

	print("Nodes Expanded: ", nodes_expanded)
	print("Execution Time", end - start_time, "Seconds")
	# import IPython
	# IPython.embed()
	# exit()
	

def print_board(matrix):
	for row in matrix:
		for char in row:
			print(char, end='')
		print()

def solve(matrix, words, initial_nodes):
	if done(matrix, words):
		print_board(matrix)
		return matrix, words, 1

	print_board(matrix)
	print()
	location = most_constrained(matrix, words) #location = (x, y, (constraints, ind)) 
	# print(location[0], location[1], location[2])
	# import IPython
	# IPython.embed()
	# exit()
	# count = 0
	expanded_nodes = 1
	for value in location[2]:
		constraint = value[0]
		index = value[1]
		new_matrix = deepcopy(matrix)
		new_matrix, start = insert_word(new_matrix, constraint, location[0], location[1])
		new_word_list = deepcopy(words)

		new_word_list[index].start = start
		new_word_list[index].orient = constraint.orient
		new_word_list[index].done = True

		solution, new_words, temp_node = solve(new_matrix, new_word_list, initial_nodes)

		expanded_nodes += temp_node

		if done(solution, new_words):
			return solution, new_words, expanded_nodes

	return matrix, words, expanded_nodes

def insert_word(matrix, constraint, row, col):
	word = constraint.word
	start = None
	if constraint.orient == 'horiz':
		temp_col = col - constraint.index
		start = (row, temp_col)
		for idx in range(len(word)):
			matrix[row][temp_col] = word[idx]
			temp_col += 1
	else:
		temp_row = row - constraint.index
		start = (temp_row, col)
		for idx in range(len(word)):
			matrix[temp_row][col] = word[idx]
			temp_row += 1

	return matrix, start

def done(matrix, word_bank):
	# for word in word_bank:
	# 	print(word.done)
	# 	if not word.done:
	# 		return False

	if not correct(matrix):
		return False

	return True

def column(matrix, i):
    return [row[i] for row in matrix]

def correct(matrix):
	for row in matrix:
		if len(row) != len(set(row)):
			return False

	for i in range(9):
		if len(column(matrix,i)) != len(set(column(matrix, i))):
			return False
			
	
	for i in [0,3,6]:
		for p in [0,3,6]:
			x = matrix[i:i+3] 
			y = []
			for m in range(3):
				y.extend(x[m][p:p+3])
			if len(y) != len(set(y)):
				return False
	return True

def most_constrained(matrix, constraints):
	global count
	solution = None

	for row in range(9):
		for col in range(9):
			if matrix[row][col] == '_':   # Possible variable
				location = (row, col, [])
				for x in range(len(constraints)):
					constraint = constraints[x]
					if not constraint.done:
						new_consts = fit(matrix, constraint, row, col)
						for const in new_consts:
							location[2].append((const, x))
				# print(len(location[2]))
				if not solution or len(solution[2]) > len(location[2]):
					solution = location

	# if count < 3:
	# print("Done", len(solution[2]))
	count += 1
	return solution

class Break(Exception): pass

def fit(matrix, constraint, row, col):
	solution = []
	horizontal = True
	vertical = True

	for index in range(len(constraint.word)):
		word = constraint.word
		char = word[index]
		
		# if not horizontal or not vertical or not threebythree(matrix, row, col, char):
		# 	continue

		if horizontal:
			temp_col = col - index
			if temp_col >= 0 and (temp_col + len(word)) <= 9:
				works = True
				try:
					for idx in range(len(word)):
						for x in range(9):
							if (x != temp_col and matrix[row][x] == word[idx]) or (x != row and matrix[x][temp_col] == word[idx]):
								raise Break
						if matrix[row][temp_col] != word[idx] and not threebythree(matrix, row, temp_col, word[idx]):#, ignore=ignore):
							raise Break
						if matrix[row][temp_col] != word[idx] and matrix[row][temp_col] != '_':
							raise Break
						temp_col += 1
				except Break:
					works = False

				if works:
					new_const = deepcopy(constraint)
					new_const.index = index
					new_const.orient = 'horiz'
					solution.append(new_const)

		if vertical: 
			temp_row = row - index
			if temp_row >= 0 and (temp_row + len(word)) <= 9:
				works = True
				try:
					for idx in range(len(word)):
						for x in range(9):
							if (x != col and matrix[temp_row][x] == word[idx]) or (x != temp_row and matrix[x][col] == word[idx]):
								raise Break
						if matrix[temp_row][col] != word[idx] and not threebythree(matrix, temp_row, col, word[idx]):#, ignore=ignore):
							raise Break
						if matrix[temp_row][col] != word[idx] and matrix[temp_row][col] != '_':
							raise Break
						temp_row += 1
				except Break:
					works = False
				if works:
					new_const = deepcopy(constraint)
					new_const.index = index
					new_const.orient = 'vert'
					solution.append(new_const)

	return solution

def threebythree(matrix, row, col, char):
	if row <= 2:
		row_range = range(0,3)
	elif row >= 6:
		row_range = range(6,9)
	else:
		row_range = range(3,6)

	if col <= 2:
		col_range = range(0,3)
	elif col >= 6:
		col_range = range(6,9)
	else:
		col_range = range(3,6)

	for r in row_range:
		for c in col_range:
			if matrix[r][c] == char:
				return False

	return True


main()