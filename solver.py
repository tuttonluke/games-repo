import numpy as np

# creates 9x9 array of integers
def input_board():
    board = []
    # input rows
    for row in range(9):
        row = input('Enter row: ')
        if len(row) != 9:
            print('Rows must have 9 integers.')
            break
        else:
            row_list = list(row)
            board.append(row_list)
    # convert data points from str to int
    for i in range(9):
        for j in range(9):
            board[i][j] = int(board[i][j])

    return board

def empty(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                return (i, j) # row, col
    return None

def possible(grid, n, yx_pos):
    for i in range(len(grid[0])):
        if grid[yx_pos[0]][i] == n and yx_pos[1] != i:
            return False # check row

    for i in range(len(grid[0])):
        if grid[i][yx_pos[1]] == n and yx_pos[0] != i:
            return False # check column

    x0 = (yx_pos[1]//3)*3
    y0 = (yx_pos[0]//3)*3

    for i in range(y0, y0 + 3):
        for j in range(x0, x0 + 3):
            if grid[i][j] == n and (i,j) != yx_pos:
                return False # check box
    return True

def solve(grid):
    find = empty(grid)
    if not find:
        return grid
    else:
        row, col = find

    for i in range(1,10):
        if possible(grid, (row, col), i):
            grid[row][col] = i

            if solve(grid):
                return grid

            grid[row][col] = 0

    return False


def solved(grid):
    find = empty(grid)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1,10):
        if possible(grid, i, (row, col)):
            grid[row][col] = i

            if solved(grid):
                return True

            grid[row][col] = 0

    return False

def valid(bo, num, pos):
    # Check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if bo[i][j] == num and (i,j) != pos:
                return False

    return True