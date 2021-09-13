def input_board():

    board = []

    for i in range(9):
        board.append(input('Enter row: '))
    return board


def row_check(board):
    for row in board:
        row_sum = 0

        for digit in row:
            row_sum += int(digit)

        if row_sum != 45:
            return False

    return True


def column_check(board):
    column_board = ['', '', '', '', '', '', '', '', '', ]
    index = 0

    while index <= 8:
        for row in range(len(board)):
            column_board[index] += board[row][index]
        index += 1

    return row_check(column_board)


def boxes_check(board):
    boxes_board = ['', '', '', '', '', '', '', '', '', ]

    for row in range(3):
        boxes_board[0] += board[row][0:3]
    for row in range(3):
        boxes_board[1] += board[row][3:6]
    for row in range(3):
        boxes_board[2] += board[row][6:9]
    for row in range(3):
        boxes_board[3] += board[row + 3][0:3]
    for row in range(3):
        boxes_board[4] += board[row + 3][3:6]
    for row in range(3):
        boxes_board[5] += board[row + 3][6:9]
    for row in range(3):
        boxes_board[6] += board[row + 6][0:3]
    for row in range(3):
        boxes_board[7] += board[row + 6][3:6]
    for row in range(3):
        boxes_board[8] += board[row + 6][6:9]

    return row_check(boxes_board)


def sudoku_check():
    board = input_board()

    if boxes_check(board) and column_check(board) and boxes_check(board) == True:
        return True
    else:
        return False


def sudoku_check_board(board):
    if boxes_check(board) and column_check(board) and boxes_check(board) == True:
        return True
    else:
        return False
