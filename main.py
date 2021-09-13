import pygame as pg
import os
import time
import random

pg.init()
pg.font.init()
pg.display.set_caption('Tetris')

# Dimensions and Variables
WIDTH, HEIGHT = 400, 720
WINDOW = pg.display.set_mode((WIDTH, HEIGHT))
GAP = WIDTH / 10

# Fonts
title_font = pg.font.SysFont('timesnewroman', 30)
time_font = pg.font.SysFont('timesnewroman', 40)

# Colours
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# Load Images
BLUE_J_BLOCK = pg.image.load(os.path.join('assets', 'blue_j_block.png'))
BACKGROUND = pg.transform.scale(pg.image.load(os.path.join('assets', 'background-black.png')), (WIDTH, HEIGHT))


class Block:

    COLOUR_MAP = {
        'blue': BLUE_J_BLOCK
    }

    def __init__(self, x, y, colour):
        self.x = x
        self.y = y
        self.GAP = HEIGHT

    def move(self):
        self.y += GAP


def format_time(secs):
    second = secs % 60
    minute = secs // 60

    if second < 10:
        total_time = ' ' + str(minute) + ':' + '0' + str(second)
    else:
        total_time = ' ' + str(minute) + ':' + str(second)

    return total_time


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


def main():
    run = True
    lost = False
    lost_count = 0
    fps = 60
    start = time.time()

    blocks = []  # stores block positions

    def redraw_window(win, time_played):
        win.blit(BACKGROUND, (0, 0))
        # display grid lines
        line_thickness = 1
        for i in range(16):  # horizontal
            pg.draw.line(win, GREY, (0, (i + 1) * GAP), (WIDTH, (i + 1) * GAP), line_thickness)
        for i in range(11):  # vertical
            pg.draw.line(win, GREY, (i * GAP, 0), (i * GAP, HEIGHT - 80), line_thickness)
        # display time
        time_text = time_font.render('Time: ' + format_time(time_played), True, WHITE)
        win.blit(time_text, (WIDTH - time_text.get_width() - 10, HEIGHT - 60))

        pg.display.update()

    while run:
        play_time = round(time.time() - start)
        redraw_window(WINDOW, play_time)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        if lost:
            if lost_count > fps * 3:
                run = False
            else:
                continue

        # while loop for incoming blocks
        block = Block(200, 0, random.choice(['blue']))
        blocks.append(block)

        for block in blocks:
            block.move()

    pg.quit()


def main_menu():
    run = True
    while run:
        WINDOW.blit(BACKGROUND, (0, 0))
        title_label = title_font.render('Click Mouse to Begin...', True, WHITE)
        WINDOW.blit(title_label, ((WIDTH / 2) - (title_label.get_width() / 2), (HEIGHT / 2)))
        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                main()
    pg.quit()


main_menu()
