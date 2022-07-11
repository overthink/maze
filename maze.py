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

# recursive backtracking
def mazify_rec(grid: List[List[int]], row: int, col: int) -> None:
    """Carve a maze into grid starting at (row, col)."""
    row_count = len(grid)
    col_count = len(grid[0])

    # randomly carve through each wall of this cell as long as we've
    # not yet vistied the destination cell
    dirs = [N, E, S, W]
    random.shuffle(dirs)
    for d in dirs:
        next_row = row + ROW_OFFSET[d]
        next_col = col + COL_OFFSET[d]
        if next_row >= 0 and next_row < row_count and \
           next_col >= 0 and next_col < col_count and \
           grid[next_row][next_col] == 0:
            grid[row][col] |= d
            grid[next_row][next_col] |= OPPOSITE[d]
            mazify_rec(grid, next_row, next_col)

def mazify_kruskal(grid: List[List[int]]) -> None:
    row_count = len(grid)
    col_count = len(grid[0])
    # generate all our edges
    edges = []
    for row in range(row_count):
        for col in range(col_count):
            for d in [N, E, S, W]:
                other_row = row + ROW_OFFSET[d]
                other_col = col + COL_OFFSET[d]
                if other_row >= 0 and other_row < row_count and \
                   other_col >= 0 and other_col < col_count:
                    edges.append((row, col, d))

    # now we'll make an inline DSU/union-find for use in the actual algo
    # We'll identify cells with id == row*col_count + col

    # parent[i] points to the representative set for cell id i
    parent = [i for i in range(row_count * col_count)] # cells start off disjoint
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
        set1 = find_set(row * col_count + col)
        set2 = find_set(other_row * col_count + other_col)
        if set1 != set2:
            union_set(set1, set2)
            grid[row][col] |= d
            grid[other_row][other_col] |= OPPOSITE[d]

def print_maze(grid: List[List[int]]) -> None:
    row_count = len(grid)
    col_count = len(grid[0])
    print(" ", "_" * (col_count * 2 - 1))
    for row in range(row_count):
        print("|", end="")
        for col in range(col_count):
            if grid[row][col] & S != 0:
                print(" ", end="")
            else:
                print("_", end="")
            if grid[row][col] & E != 0:
                if (grid[row][col] | grid[row][col+1]) & S != 0:
                    print(" ", end="")
                else:
                    print("_", end="")
            else:
                print("|", end="")
        print("")

def main() -> None:
    size = 20
    # cell value of 0 means unvisited/"uncarved"
    grid = [[0] * size for _ in range(size)]
    # mazify_rec(grid, 0, 0)
    mazify_kruskal(grid)
    print_maze(grid)

if __name__ == "__main__":
    main()
