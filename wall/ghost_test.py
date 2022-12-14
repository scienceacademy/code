STRIP = False

import sys
from PIL import Image
from itertools import cycle
from random import choice, random, randint
import pygame as pg
vec2 = pg.Vector2
if STRIP:
    from rpi_ws281x import PixelStrip, Color

from sprite_data import *
## LED MATRIX SETTINGS
LED_COUNT = 400
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False
LED_CHANNEL = 0
ROTATION = 0

if STRIP:
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA,
                       LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(0,0,0))
    strip.show()

WIDTH = 400
HEIGHT = 400
PIXEL = 20
FPS = 10

def check_valid_pos(pos):
    return 0 >= pos.x >= 19 and 0 >= pos.y >= 19

class sprite_data:
    def __init__(self, fnames, pos, anim_speed, loop=True):
        self.frames = []
        for f in fnames:
            img = Image.open(f)
            self.width, self.height = img.size
            self.frames.append(list(img.getdata()))
        self.anim = cycle(self.frames)
        self.anim_speed = anim_speed
        self.current_frame = self.frames[0]
        self.pos = pos
        self.last_update = 0
        self.frame_count = 0
        self.loop = loop
        self.done = False

    def move(self, dir):
        self.pos += dir

    def draw(self, flipped=False):
        now = pg.time.get_ticks()
        if now - self.last_update > self.anim_speed:
            self.last_update = now
            self.current_frame = next(self.anim)
            self.frame_count += 1
        if not self.loop and self.frame_count == len(self.frames):
            self.done = True
        if not flipped:
            for x in range(self.width):
                for y in range(self.height):
                    # if check_valid_pos(vec2(x+self.pos.x, y+self.pos.y)):
                    c = self.current_frame[self.width * y + x]
                    draw_pixel(x + self.pos.x, y + self.pos.y, c)
        else:
            for x in range(self.width-1, -1, -1):
                for y in range(self.height):
                    # if check_valid_pos(vec2(x+self.pos.x, y+self.pos.y)):
                    c = self.current_frame[self.width * y + x]
                    draw_pixel(self.width-x + self.pos.x, y + self.pos.y, c)

pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

layout = [[i + j * 20 for i in range(20)] for j in range(20)]
for row in range(20):
    if row % 2 == 1:
        layout[row].reverse()
# for row in layout:
#     print(row)


pm = sprite_data(
    ["pm_sprites/pm1.png", "pm_sprites/pm2.png", "pm_sprites/pm3.png"], vec2(20, 5), 125)
blinky = sprite_data(
    ["pm_sprites/blinky1.png", "pm_sprites/blinky2.png"], vec2(20, 5), 250)
pinky = sprite_data(
    ["pm_sprites/pinky1.png", "pm_sprites/pinky2.png"], vec2(20, 5), 250)
inky = sprite_data(
    ["pm_sprites/inky1.png", "pm_sprites/inky2.png"], vec2(20, 5), 250)
clyde = sprite_data(
    ["pm_sprites/clyde1.png", "pm_sprites/clyde2.png"], vec2(20, 5), 250)
flee1 = sprite_data(
    ["pm_sprites/flee1.png", "pm_sprites/flee2.png"], vec2(20, 5), 250)
flee2 = sprite_data(
    ["pm_sprites/flee1.png", "pm_sprites/flee2.png"], vec2(20, 5), 250)
flee3 = sprite_data(
    ["pm_sprites/flee1.png", "pm_sprites/flee2.png"], vec2(20, 5), 250)
flee4 = sprite_data(
    ["pm_sprites/flee1.png", "pm_sprites/flee2.png"], vec2(20, 5), 250)

def clear_strip():
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

def draw_pixel_strip(x, y, col):
    if ROTATION == 0:
        n = x + y * 20
    elif ROTATION == 90:
        n = 19 + x * 20 - y
    elif ROTATION == 180:
        n = 399 - x - y * 20
    elif ROTATION == -90:
        n = 380 - x * 20 + y
    try:
        n = layout[int(y)][int(x)]
    except IndexError:
        # print(x, y, n)
        n = 1
    c = Color(col[1], col[0], col[2])
    strip.setPixelColor(int(n), c)

def draw_pixel(x, y, col):
    # r = pg.Rect(x * PIXEL, y * PIXEL, PIXEL, PIXEL)
    # pg.draw.rect(screen, col, r, border_radius=6)
    pg.draw.circle(screen, col,
            (int(x) * PIXEL + PIXEL//2,
            int(y) * PIXEL + PIXEL//2),
            int(PIXEL/2 * 0.9))
    if STRIP:
        draw_pixel_strip(x, y, col)

def pm_anim2():
    print("starting pacman2")
    FPS = 15
    flee1.pos = vec2(20, 5)
    pm.pos = vec2(20+(14+5)*1, 5)
    done = False
    while not done:
        clock.tick(FPS)
        if STRIP:
            clear_strip()
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                pg.quit()
                sys.exit()
        pm.move(vec2(-2.1, 0))
        flee1.move(vec2(-2, 0))
        screen.fill((0, 0, 0))
        pm.draw(True)
        flee1.draw()
        if pm.pos.x < -25 and not pg.mixer.get_busy():
            print("fin2")
            done = True
        pg.display.flip()
        if STRIP:
            strip.show()
    pg.mixer.music.fadeout(1000)

def pm_anim1():
    # ghosts chase pm to left
    print("starting pacman1")
    pg.mixer.music.load("pm_sounds/intermission.wav")
    pg.mixer.music.play(2)
    FPS = 15
    pm.pos = vec2(-14, 5)
    g = choice([inky, pinky, blinky, clyde])
    g.pos = vec2((-14-7)*2, 5)
    # inky.pos = vec2((-14-5)*2, 5)
    # pinky.pos = vec2((-14-5)*3, 5)
    # blinky.pos = vec2((-14-5)*4, 5)
    # clyde.pos = vec2((-14-5)*5, 5)
    done = False
    while not done:
        clock.tick(FPS)
        if STRIP:
            clear_strip()
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                pg.quit()
                sys.exit()
        pm.move(vec2(2, 0))
        g.move(vec2(2, 0))
        # inky.move(vec2(2, 0))
        # pinky.move(vec2(2, 0))
        # blinky.move(vec2(2, 0))
        # clyde.move(vec2(2, 0))
        screen.fill((0, 0, 0))
        pm.draw()
        g.draw(True)
        # inky.draw(True)
        # pinky.draw(True)
        # blinky.draw(True)
        # clyde.draw(True)
        if g.pos.x > 30:
            print("fin1")
            done = True
        pg.display.flip()
        if STRIP:
            strip.show()
    pm_anim2()


def boo_anim():
    print("starting boo")
    m_ghost = sprite_data(
        ["m_sprites/mario_ghost.png"], vec2(20, 4), 250)
    m_ghost_seq = [vec2(-2, 0), vec2(0, -1), vec2(-2, 0), vec2(0, 1),
                    vec2(-2, 0), vec2(0, -1), vec2(-2, 0), vec2(0, 1)
                    ]
    m_ghost_moves = cycle(m_ghost_seq)
    boo_laugh = pg.mixer.Sound("m_sprites/Boo_Laugh_1.ogg")

    playing = True
    boo_laugh.play()
    reverse = False
    while playing:
        clock.tick(FPS)
        if STRIP:
            clear_strip()
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                pg.quit()
                sys.exit()
        if pg.time.get_ticks() % 20 == 0 and random() > 0.65:
            boo_laugh.play()
        m = next(m_ghost_moves)
        if reverse:
            m = -m
        m_ghost.move(m)
        if m_ghost.pos.x < -30:
            m_ghost.pos.x = -30
            m_ghost.pos.y = randint(-2, 6)
            reverse = not reverse
        if m_ghost.pos.x > 25:
            m_ghost.pos.x = 25
            m_ghost.pos.y = randint(-2, 6)
            reverse = not reverse
            if random() > 0.6:
                playing = False
        screen.fill((0, 0, 0))
        m_ghost.draw(not reverse)
        pg.display.flip()
        if STRIP:
            strip.show()

def bowser():
    print("starting bowser")
    if STRIP:
            clear_strip()
    bow = sprite_data(
        ["m_sprites/bowser1.png"], vec2(0, 0), 250)
    bow_laugh = pg.mixer.Sound("m_sprites/SM64_Bowser_Laugh.ogg")

    bow_laugh.play()
    clock.tick(FPS)
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            pg.quit()
            sys.exit()
    screen.fill((0, 0, 0))
    bow.draw()
    pg.display.flip()
    if STRIP:
        strip.show()
    # pg.time.wait(5000)

def creeper():
    print("starting creeper")
    if STRIP:
            clear_strip()
    cr = sprite_data(
        ["m_sprites/creeper.png"], vec2(0, 0), 250)
    # cr_sound = pg.mixer.Sound("m_sprites/creeper_explosion.mp3")
    clock.tick(FPS)
    # cr_sound.play()
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            pg.quit()
            sys.exit()
    screen.fill((0, 0, 0))
    cr.draw()
    pg.display.flip()
    if STRIP:
        strip.show()
    # pg.time.wait(6000)


def zombie():
    f_list = [f"zombie/sprite_{i:02}.png" for i in range(25)]
    z = sprite_data(f_list, vec2(0, 0), 250, False)
    zs2 = pg.mixer.Sound("misc_sounds/brains.wav")
    playing = True
    while playing:
        clock.tick(FPS)
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                pg.quit()
                sys.exit()
        screen.fill((0, 0, 0))
        z.draw()
        if z.frame_count == 7:
            zs2.play()
        if z.done:
            playing = False
        pg.display.flip()
        if STRIP:
            strip.show()


animations = [pm_anim1, bowser, creeper, boo_anim, zombie]
while True:
    choice(animations)()
    pg.time.wait(2000) # loop ?
# zombie()
pg.quit()