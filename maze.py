"""Maze generator
Based on: https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking

Mostly just messing around with typechecked python.
"""

from typing import *
import random

# Direction "flags". Used to indicate which edges of a grid cell have walls.
N, E, S, W = 1, 2, 4, 8

# Yields the value to add to current row/col to go in a given direction.
ROW_OFFSET = {N: -1, E: 0, S: 1, W: 0}
COL_OFFSET = {N: 0, E: 1, S: 0, W: -1}

OPPOSITE = {N: S, E: W, S: N, W: E}

# recursive backtracking
def mazify(grid: List[List[int]], row: int, col: int) -> None:
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
            mazify(grid, next_row, next_col)

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
    mazify(grid, 0, 0)
    print_maze(grid)

if __name__ == "__main__":
    main()
