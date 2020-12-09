import random
import sys
from typing import List, Optional


def solve(N: int) -> None:
	iters = 100*N
	displaySolution(min_conflicts(N, iters), N)

def displaySolution(queens: List[int], N: int):
	resultToDisplay = []
	for col in range(N):
		row = ['_'] * N
		resultToDisplay.append(row)

	for col in range(N):
		resultToDisplay[queens[col]][col] = 'Q'

	for col in range(N):
		print(resultToDisplay[col])


# removing queen from position = row, col
def update_arrays_on_remove(row, col, N, r: List[str], d1: List[str], d2: List[str]):
	r[row] -= 1
	d1[row - col + N - 1] -= 1
	d2[row + col] -= 1

# adding queen to position = row, col
def update_arrays_on_add(row, col, N, r: List[str], d1: List[str], d2: List[str]):
	r[row] += 1
	d1[row - col + N - 1] += 1
	d2[row + col] += 1


def initQueens(N: int, r: List[int], d1: List[int], d2: List[int]) -> List[int]:
	queens = [-1] * N
	for col in range(N):
		# TODO row has to be not used until now ?
		row = getRowWithMinConflicts(col, queens, N, r, d1, d2)
		queens[col] = row
		update_arrays_on_add(queens[col], col, N, r, d1, d2)

	return queens

def random_pos(list, N, filter):
		return random.choice([i for i in range(N) if filter(list[i])])

def min_conflicts(N: int, iters: int):	

	r = [0 for i in range(N)]
	d1 = [0 for i in range(2 * N - 1)]
	d2 = [0 for i in range(2 * N - 1)]

	queens = initQueens(N, r, d1, d2)

	for k in range(iters):
		
		col = getColWithMaxConflicts(queens, N, r, d1, d2)
		if col is None:
			# found solution
			return queens

		update_arrays_on_remove(queens[col], col, N, r, d1, d2)
		newRow = getRowWithMinConflicts(col, queens, N, r, d1, d2)

		queens[col] = newRow
		update_arrays_on_add(queens[col], col, N, r, d1, d2)


	raise Exception("Incomplete solution: try more iterations.")

def getColWithMaxConflicts(queens, N, r, d1, d2) -> Optional[int]:
	confs = compute_conflicts_for_each_queen(queens, N, r, d1, d2)
	if sum(confs) == 0:
		return None
	
	# taking the queen with max conflicts
	return random_pos(confs, N, lambda elt: elt == max(confs))

def getRowWithMinConflicts(col: int, queens: List[int], N: int, r: List[int], d1: List[int], d2: List[int]) -> int:
	queenConflictsAfterEventualNextStep = []
	minConfl = sys.maxsize
	# computing the eventual conflicts for each possible next step
	for row in range(N):
		queens[col] = row

		update_arrays_on_add(queens[col], col, N, r, d1, d2)

		newConfl = compute_conflicts_given_queen(col, row, N, r, d1, d2)
		queenConflictsAfterEventualNextStep.append(newConfl)
		minConfl = min(minConfl, newConfl)

		update_arrays_on_remove(queens[col], col, N, r, d1, d2)

	return random_pos(queenConflictsAfterEventualNextStep, N, lambda elt: elt == minConfl)

def compute_conflicts_for_each_queen(queens, N, r, d1, d2):
	# TODO and return max_conflict for optimization

    return [compute_conflicts_given_queen(col, queens[col], N, r, d1, d2) for col in range(N)]

def compute_conflicts_given_queen(queenColumn, queenRow, N, r, d1, d2):
	return r[queenRow] - 1 + d1[queenRow - queenColumn + N - 1] - 1 + d2[queenRow + queenColumn] - 1



solve(1000)