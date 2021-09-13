import pygame as pg, time
from solver import possible, solved, solve

pg.init()
pg.font.init()

BLACK = (0, 0, 0)
GREY = (128, 128, 128)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

time_font = pg.font.SysFont('timesnewroman', 40)
lost_font = pg.font.SysFont('timesnewroman', 100)

class Grid:

    board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
          ]

    # board = [
    #     [5, 3, 4, 6, 7, 8, 9, 1, 2],
    #  [6, 7, 2, 1, 9, 5, 3, 4, 8],
    #  [1, 9, 8, 3, 4, 2, 5, 6, 7],
    #  [8, 5, 9, 7, 6, 1, 4, 2, 3],
    #  [4, 2, 6, 8, 5, 3, 7, 9, 1],
    #  [7, 1, 3, 9, 2, 4, 8, 5, 6],
    #  [9, 6, 1, 5, 3, 7, 2, 8, 4],
    #  [2, 8, 7, 4, 1, 9, 6, 3, 5],
    #  [3, 4, 5, 2, 8, 6, 1, 7, 0]
    #          ]

    # board = input_board()

    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.selected = None

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if possible(self.model, val, (row, col)) and solved(self.model) == True:
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self, win):
        # grid lines
        gap = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                line_thickness = 4
            else:
                line_thickness = 1
            pg.draw.line(win, BLACK, (0, i * gap), (self.width, i * gap), line_thickness)
            pg.draw.line(win, BLACK, (i * gap, 0), (i * gap, self.height), line_thickness)
        # squares
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)

    def select(self, row, col):
        # reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False
        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        if pos[0] < self.width and pos[0] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y), int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True

class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = time_font.render(str(self.temp), 1, GREY)
            win.blit(text, (x + 5, y + 5))
        elif not (self.value == 0):
            text = time_font.render(str(self.value), 1, BLACK)
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))
        if self.selected:
            pg.draw.rect(win, RED, (x, y, gap, gap), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val

def redraw_window(win, board, time):
    WIDTH = 540
    HEIGHT = 600
    if board.is_finished():
        win.fill(WHITE)
        game_over_label = lost_font.render('Game Over!', True, BLACK)
        win.blit(game_over_label, ((WIDTH / 2) - game_over_label.get_width() / 2, (HEIGHT / 2) - 50))
        return
    win.fill(WHITE)
    text = time_font.render('Time: ' + format_time(time), 1, BLACK)
    win.blit(text, (540 - 200, 550))
    board.draw(win)

    text = time_font.render('SOLVE', 1, RED)
    win.blit(text, (20, 550))
    pg.draw.rect(win, RED, (15, 550, text.get_width() + 10, text.get_height()), 3)

def format_time(secs):
    sec = secs % 60
    minute = secs // 60
    hour = minute // 60

    if sec < 10:
        mat = ' ' + str(minute) + ':' + '0' + str(sec)
    else:
        mat = ' ' + str(minute) + ':' + str(sec)

    return mat

def main():
    WIDTH = 540
    HEIGHT = 600
    win = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption('Sudoku')
    board = Grid(9, 9, 540, 540)
    key = None
    run = True
    start = time.time()
    # strikes = 0
    while run:

        play_time = round(time.time() - start)

        if board.selected and key != None:
            board.sketch(key)
            key = None

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_1 or event.key == pg.K_KP1:
                     key = 1
                if event.key == pg.K_2 or event.key == pg.K_KP2:
                    key = 2
                if event.key == pg.K_3 or event.key == pg.K_KP3:
                    key = 3
                if event.key == pg.K_4 or event.key == pg.K_KP4:
                    key = 4
                if event.key == pg.K_5 or event.key == pg.K_KP5:
                    key = 5
                if event.key == pg.K_6 or event.key == pg.K_KP6:
                    key = 6
                if event.key == pg.K_7 or event.key == pg.K_KP7:
                    key = 7
                if event.key == pg.K_8 or event.key == pg.K_KP8:
                    key = 8
                if event.key == pg.K_9 or event.key == pg.K_KP9:
                    key = 9

                if board.selected:
                    row, col = board.selected
                    if event.type == pg.K_UP:
                        if row > 0:
                            board.select(row - 1, col)
                            row -= 1
                        else:
                            row = 0
                    if event.key == pg.K_RIGHT:
                        if col < 8:
                            board.select(row, col + 1)
                        else:
                            col = 8
                    if event.key == pg.K_DOWN:
                        if row < 8:
                            board.select(row + 1, col)
                        else:
                            row = 8
                    if event.key == pg.K_LEFT:
                        if col > 0:
                            board.select(row, col - 1)
                        else:
                            col = 0

                if event.key == pg.K_DELETE or event.key == pg.K_BACKSPACE:
                    board.clear()
                    key = None
                if event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp) == True:
                            print('Success')
                        else:
                            print('Wrong')
                        key = None
            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                x, y = pos
                if y < 540:
                    clicked = board.click(pos)
                    if clicked:
                        board.select(clicked[0], clicked[1])
                        key = None
                else:
                    text = time_font.render('SOLVE', 1, RED)
                    if 15 < x < text.get_width() + 25 and 550 < y < 550 + text.get_height():
                        grid = board.model
                        win.fill(WHITE)
                        for i in range(9):
                            for j in range(9):
                                output = grid[i][j]
                                n_text = time_font.render(str(output), 1, BLACK)
                                win.blit(n_text, pg.Vector2((j * 60), (i * 60)))




        redraw_window(win, board, play_time)
        pg.display.update()

main()
pg.quit()

# solve button, up key bug