import os
# os.environ['SDL_AUDIODRIVER'] = "pulse"
STRIP = True

import pygame as pg
vec2 = pg.Vector2
from time import sleep
from random import choice, random
from itertools import cycle
if STRIP:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BOARD)
    from rpi_ws281x import PixelStrip, Color

## LED MATRIX SETTINGS
LED_COUNT = 400
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False
LED_CHANNEL = 0
ROTATION = 90
buttons = {
    16: pg.K_LEFT,
    18: pg.K_RIGHT,
    22: pg.K_UP,
    24: pg.K_DOWN
}

if STRIP:
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA,
                       LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()

## GAME SETTINGS
WIDTH = 400
HEIGHT = 400
PIXEL = 20
FPS = 5
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GREY = (100,100,100)
BLUE = (25, 25, 166)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
PINK = (255, 193, 204)
CYAN = (0, 255, 255)
ORANGE = (255, 166, 0)
DKBLUE = (3, 79, 254)
WALL = BLUE
PM = YELLOW
PILL = GREY
POWPILL = WHITE
INKY = CYAN
PINKY = PINK
BLINKY = RED
CLYDE = ORANGE

moves = {
    pg.K_UP: vec2(0, -1),
    pg.K_DOWN: vec2(0, 1),
    pg.K_RIGHT: vec2(1, 0),
    pg.K_LEFT: vec2(-1, 0)
}

board_colors = {
    0: BLACK,
    1: WALL,
    2: PILL,
    3: POWPILL
}


pg.init()
pg.mixer.init(44100, -16, 1, 1024)
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

sounds = {
    "start": pg.mixer.Sound("pm_sounds/game_start.wav"),
    "munch1": pg.mixer.Sound("pm_sounds/munch_1.wav"),
    "munch2": pg.mixer.Sound("pm_sounds/munch_2.wav"),
    "pow": pg.mixer.Sound("pm_sounds/power_pellet.wav"),
    "death": pg.mixer.Sound("pm_sounds/death_all.wav"),
    "siren": pg.mixer.Sound("pm_sounds/siren_1.wav"),
    "flee": pg.mixer.Sound("pm_sounds/retreating.wav")

}
munch_sounds = cycle([sounds["munch1"], sounds["munch2"]])

maze = """
1111111111111111111
1222222222222222221
1311212111112121131
1222212221222122221
1111211121211121111
0001212222222121000
0001212110112121000
0001212100012121000
1111212100012121111
0000222111112220000
1111212222222121111
0001212111112121000
0001212222222121000
1111212111112121111
1222222221222222221
1211211121211121121
1231222222222221321
1121212111112121211
1122212222222122211
1111111111111111111
"""

layout = [[i + j * 20 for i in range(20)] for j in range(20)]
for row in range(20):
    if row % 2 == 1:
        layout[row].reverse()
# for row in layout:
#     print(row)


def check_buttons():
    for butt in buttons:
        state = GPIO.input(butt)
        if state == 0:
            ev = pg.event.Event(pg.KEYDOWN, key=buttons[butt])
            pg.event.post(ev)

def draw_pixel_strip(x, y, col):
    if ROTATION == 0:
        n = layout[int(y)][int(x)]
    elif ROTATION == -90:
        # n = 19 + x * 20 - y
        r = [[layout[j][i] for j in range(len(layout))] for i in range(len(layout[0])-1, -1, -1)]
        n = r[int(y)][int(x)]
    elif ROTATION == 90:
        r = [[layout[j][i] for j in range(len(layout))] for i in range(len(layout[0]))]
        n = r[int(y)][int(x)]
    c = Color(col[1], col[0], col[2])
    strip.setPixelColor(int(n), c)

def draw_pixel(x, y, col):
    # r = pg.Rect(x * PIXEL, y * PIXEL, PIXEL, PIXEL)
    # pg.draw.rect(screen, col, r, border_radius=6)
    pg.draw.circle(screen, col, (int(x) * PIXEL + PIXEL//2,
                   int(y) * PIXEL + PIXEL//2), int(PIXEL//2 * 0.9))
    if STRIP:
        draw_pixel_strip(x, y, col)


class Board:
    def __init__(self):
        self.board = []
        for i in maze.strip().split("\n"):
            self.board.append([int(n) for n in i])
        self.pills = 0
        for row in self.board:
            self.pills += row.count(2)
        print("pills:", self.pills)

    def get_cell(self, cell):
        return self.board[int(cell.y)][int(cell.x)]

    def set_cell(self, cell, n):
        self.board[int(cell.y)][int(cell.x)] = n

    def draw(self):
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                draw_pixel(x, y, board_colors[cell])
        # draw score (remaining pills)
        pills_left = 0
        # for row in self.board:
        #     pills_left += row.count(2)
        # pct = int((20 / self.pills) * (self.pills - pills_left))
        # for i in range(pct):
        #     draw_pixel(19, 20-i, GREEN)


class Ghost:
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color
        self.orig_color = color
        self.scared = False
        self.dir = choice(list(moves.values()))

    def move(self):
        if random() > 0.5:
            self.dir = choice(list(moves.values()))
        while True:
            # if self.pos + self.dir in [vec2(3, 9), vec2(15, 9)]:
            if (self.pos.x + self.dir.x) in [-1, 18] or (self.pos.y + self.dir.y) in [-1, 19]:
                self.dir = choice(list(moves.values()))
            elif board.get_cell(self.pos + self.dir) != 1:
                break
            else:
                self.dir = choice(list(moves.values()))
        self.pos += self.dir

    def flee(self):
        self.color = DKBLUE
        self.scared = True

    def reset(self):
        self.color = self.orig_color
        self.scared = False

    def kill(self):
        self.reset()
        self.pos = vec2(9, 8)
        # self.pos = vec2(17, 9)

    def draw(self):
        draw_pixel(self.pos.x, self.pos.y, self.color)

class Pacman:
    def __init__(self):
        self.pos = vec2(9, 16)
        self.dir = vec2(0, 0)
        self.pow_timer = 0

    def move(self):
        if self.pow_timer > 0:
            self.pow_timer -= 1
            if self.pow_timer <= 0:
                self.pow_timer = 0
                for ghost in ghosts:
                    ghost.reset()
        if self.dir.length() == 0:
            return
        newpos = self.pos + self.dir
        # wraparound
        if newpos == vec2(-1, 9):
            self.pos = vec2(18, 9)
            return
        if newpos == vec2(19, 9):
            self.pos = vec2(0, 9)
            return
        # is there a wall there?
        if board.get_cell(newpos) != 1:
            self.pos += self.dir
            # pickup?
            c = board.get_cell(self.pos)
            if c == 2:
                board.set_cell(self.pos, 0)
                next(munch_sounds).play()
            if c == 3:
                board.set_cell(self.pos, 0)
                sounds["pow"].play()
                self.pow_timer = 50
                for ghost in ghosts:
                    ghost.flee()
        else:
            self.dir = vec2(0, 0)

    def draw(self):
        draw_pixel(self.pos.x, self.pos.y, PM)

def check_collisions():
    global dead
    # check for ghost/player collision
    for ghost in ghosts:
        if ghost.pos == pm.pos:
            if ghost.scared:
                ghost.kill()
            elif not dead:
                print("gotcha")
                dead = True
                bg_channel.stop()
                bg_channel.play(sounds["death"])
                bg_channel.set_endevent(pg.USEREVENT+1)

board = Board()
pm = Pacman()
inky = Ghost(vec2(7, 10), INKY)
pinky = Ghost(vec2(7, 5), PINKY)
blinky = Ghost(vec2(11, 10), BLINKY)
clyde = Ghost(vec2(11, 5), CLYDE)

ghosts = [inky, pinky, blinky, clyde]
sounds["start"].play()
bg_channel = pg.mixer.Channel(7)
wait = True
dead = False

playing = True
while playing:
    if wait and not pg.mixer.get_busy():
        wait = False
    clock.tick(FPS)
    # get input
    for event in pg.event.get():
        if event.type == pg.QUIT:
            playing = False
        if event.type == pg.USEREVENT+1:
            playing = False
        if event.type == pg.KEYDOWN:
            if event.key in moves and board.get_cell(pm.pos + moves[event.key]) != 1:
                pm.dir = moves[event.key]

    # move ghosts, move player
    if not wait and not dead:
        for ghost in ghosts:
            ghost.move()
        check_collisions()
        pm.move()
        check_collisions()

        if pm.pow_timer > 0:
            bg_channel.queue(sounds["flee"])
        else:
            bg_channel.queue(sounds["siren"])

    # update screen
    screen.fill(BLACK)
    board.draw()
    pm.draw()
    for ghost in ghosts:
        ghost.draw()
    pg.display.flip()
    # update matrix
    if STRIP:
        strip.show()

pg.quit()
