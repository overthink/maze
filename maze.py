"""Maze generator
Based on: https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking

Mostly just messing around with typechecked python.
"""

from typing import *
import random

# Direction "flags". Used to indicate which edges of a grid cell have openings.
N, E, S, W = 1, 2, 4, 8

# Yields the value to add to current row/col to go in a given direction.
ROW_OFFSET = {N: -1, E: 0, S: 1, W: 0}
COL_OFFSET = {N: 0, E: 1, S: 0, W: -1}

OPPOSITE = {N: S, E: W, S: N, W: E}

class Grid:
    def __init__(self, row_count: int, col_count: int) -> None:
        self.row_count = row_count
        self.col_count = col_count
        # 0 means the cell has no connections to neighbours yet
        self.data = [[0] * col_count for _ in range(row_count)]

# recursive backtracking
def mazify_rec(grid: Grid, row: int, col: int) -> None:
    """Carve a maze into grid starting at (row, col)."""
    # randomly carve through each wall of this cell as long as we've
    # not yet vistied the destination cell
    dirs = [N, E, S, W]
    random.shuffle(dirs)
    for d in dirs:
        next_row = row + ROW_OFFSET[d]
        next_col = col + COL_OFFSET[d]
        if next_row >= 0 and next_row < grid.row_count and \
           next_col >= 0 and next_col < grid.col_count and \
           grid.data[next_row][next_col] == 0:
            grid.data[row][col] |= d
            grid.data[next_row][next_col] |= OPPOSITE[d]
            mazify_rec(grid, next_row, next_col)

def mazify_kruskal(grid: Grid) -> None:
    # generate all our edges
    edges = []
    for row in range(grid.row_count):
        for col in range(grid.col_count):
            for d in [N, E, S, W]:
                other_row = row + ROW_OFFSET[d]
                other_col = col + COL_OFFSET[d]
                if other_row >= 0 and other_row < grid.row_count and \
                   other_col >= 0 and other_col < grid.col_count:
                    edges.append((row, col, d))

    # now we'll make an inline DSU/union-find for use in the actual algo
    # We'll identify cells with id == row*col_count + col

    # parent[i] points to the representative set for cell id i
    parent = [i for i in range(grid.row_count * grid.col_count)]
    def find_set(cell_id: int) -> int:
        if parent[cell_id] == cell_id:
            return cell_id
        # path compression
        parent[cell_id] = find_set(parent[cell_id])
        return parent[cell_id]

    def union_set(set_a: int, set_b: int) -> None:
        if set_a != set_b:
            parent[set_b] = set_a
        # should do union by size...

    # randomize the edges and execute Kruskal's algo
    random.shuffle(edges)
    while edges:
        row, col, d = edges.pop()
        other_row = row + ROW_OFFSET[d]
        other_col = col + COL_OFFSET[d]
        set1 = find_set(row * grid.col_count + col)
        set2 = find_set(other_row * grid.col_count + other_col)
        if set1 != set2:
            union_set(set1, set2)
            grid.data[row][col] |= d
            grid.data[other_row][other_col] |= OPPOSITE[d]

def print_maze(grid: Grid) -> None:
    print(" ", "_" * (grid.col_count * 2 - 1))
    for row in range(grid.row_count):
        print("|", end="")
        for col in range(grid.col_count):
            if grid.data[row][col] & S != 0:
                print(" ", end="")
            else:
                print("_", end="")
            if grid.data[row][col] & E != 0:
                if (grid.data[row][col] | grid.data[row][col+1]) & S != 0:
                    print(" ", end="")
                else:
                    print("_", end="")
            else:
                print("|", end="")
        print("")

def main() -> None:
    grid = Grid(20, 20)
    #mazify_rec(grid, 0, 0)
    mazify_kruskal(grid)
    print_maze(grid)

if __name__ == "__main__":
    main()
