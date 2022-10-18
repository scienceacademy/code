# from sprite_data import *
import pygame as pg
from random import choice, random, randint, shuffle
from itertools import cycle
from PIL import Image
import sys
STRIP = True

vec2 = pg.Vector2
if STRIP:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BOARD)
    from rpi_ws281x import PixelStrip, Color

quit_button = 16
if STRIP:
    GPIO.setup(quit_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

## LED MATRIX SETTINGS
LED_COUNT = 400
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False
LED_CHANNEL = 0
ROTATION = 90

if STRIP:
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA,
                       LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

WIDTH = 400
HEIGHT = 400
PIXEL = 20
FPS = 10


def check_button():
    state = GPIO.input(quit_button)
    if state == 0:
        ev = pg.event.Event(pg.KEYDOWN, key=pg.K_TAB)
        pg.event.post(ev)

def check_valid_pos(pos):
    return 0 <= pos.x <= 19 and 0 <= pos.y <= 19


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



def clear_strip():
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(0, 0, 0))
    # strip.setPixelColor(0, Color(255, 0, 0))
    # strip.show()


def draw_pixel_strip(x, y, col):
    if ROTATION == 0:
        n = layout[int(y)][int(x)]
    elif ROTATION == -90:
        # n = 19 + x * 20 - y
        r = [[layout[j][i] for j in range(len(layout))]
             for i in range(len(layout[0])-1, -1, -1)]
        n = r[int(y)][int(x)]
    elif ROTATION == 90:
        r = [[layout[j][i] for j in range(len(layout)-1, -1, -1)]
             for i in range(len(layout[0]))]
        n = r[int(y)][int(x)]
    c = Color(col[1], col[0], col[2])
    strip.setPixelColor(int(n), c)


def draw_pixel(x, y, col):
    pg.draw.circle(screen, col,
                   (int(x) * PIXEL + PIXEL//2,
                    int(y) * PIXEL + PIXEL//2),
                   int(PIXEL/2 * 0.9))
    if not check_valid_pos(vec2(x, y)):
        # print("oob", x, y)
        return
    if STRIP:
        draw_pixel_strip(x, y, col)

def check_events():
#            if not check_button():
 #               pg.quit()
  #              sys.exit()
    if STRIP:
        check_button()
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if ev.type == pg.KEYDOWN and ev.key == pg.K_TAB:
            pg.quit()
            sys.exit()


################ PACMAN ANIM
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
        check_events()
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
    done = False
    while not done:
        clock.tick(FPS)
        if STRIP:
            clear_strip()
        check_events()
        pm.move(vec2(1, 0))
        g.move(vec2(1, 0))
        screen.fill((0, 0, 0))
        pm.draw()
        g.draw(True)
        if g.pos.x > 30:
            print("fin1")
            done = True
        pg.display.flip()
        if STRIP:
            strip.show()
    pm_anim2()

############# BOO ANIMATION #################
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
        check_events()
        if pg.time.get_ticks() % 20 == 0 and random() > 0.7:
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

########### BOWSER ANIMATION #############
def bowser():
    print("starting bowser")
    if STRIP:
        clear_strip()
    bow = sprite_data(
        ["m_sprites/bowser1.png"], vec2(0, 0), 250)
    bow_laugh = pg.mixer.Sound("m_sprites/SM64_Bowser_Laugh.ogg")
    bow_laugh.play()
    start = pg.time.get_ticks()
    playing = True
    while playing:
        clock.tick(FPS)
        check_events()
        screen.fill((0, 0, 0))
        bow.draw()
        pg.display.flip()
        if STRIP:
            strip.show()
        if pg.time.get_ticks() - start > bow_laugh.get_length() * 1000 + 1500:
            playing = False
        # pg.time.wait(int(bow_laugh.get_length() * 1000) + 1500)

############ CREEPER ANIMATION
def creeper():
    print("starting creeper")
    if STRIP:
        clear_strip()
    cr = sprite_data(
        ["m_sprites/creeper.png"], vec2(0, 0), 250)
    cr_sound = pg.mixer.Sound("m_sprites/creeper_explosion.mp3")
    start = pg.time.get_ticks()
    cr_sound.play()
    playing = True
    while playing:
        clock.tick(FPS)
        check_events()
        screen.fill((0, 0, 0))
        cr.draw()
        pg.display.flip()
        if STRIP:
            strip.show()
        if pg.time.get_ticks() - start > cr_sound.get_length() * 1000 + 1500:
            playing = False
    # pg.time.wait(int(cr_sound.get_length() * 1000))

########## ZOMBIE ANIMATION
def zombie():
    f_list = [f"zombie/sprite_{i:02}.png" for i in range(25)]
    z = sprite_data(f_list, vec2(0, 0), 250, False)
    zs2 = pg.mixer.Sound("misc_sounds/brains.wav")
    playing = True
    while playing:
        clock.tick(FPS)
        check_events()
        if STRIP:
            clear_strip()
        screen.fill((0, 0, 0))
        z.draw()
        if z.frame_count == 7:
            zs2.play()
        if z.done:
            playing = False
        pg.display.flip()
        if STRIP:
            strip.show()

########## MACY PUMPKIN ######
def macy_pumpkin():
    f_list = [f"macy_pumpkin/sprite_{i:02}.png" for i in range(57)]
    mp = sprite_data(f_list, vec2(0, 0), 250, False)
    start = pg.time.get_ticks()
    playing = True
    while playing:
        clock.tick(FPS)
        if STRIP:
            clear_strip()
        check_events()
        screen.fill((0, 0, 0))
        mp.draw()
        if mp.done:
            playing = False
        pg.display.flip()
        if STRIP:
            strip.show()
        # if pg.time.get_ticks() - start > 15000:
        #     playing = False

########## SASHA ######
def sasha():
    f_list = [f"sasha/pixil-frame-{i}.png" for i in range(40)]
    mp = sprite_data(f_list, vec2(0, 0), 250, False)
    playing = True
    while playing:
        clock.tick(FPS)
        if STRIP:
            clear_strip()
        check_events()
        screen.fill((0, 0, 0))
        mp.draw()
        if mp.done:
            playing = False
        pg.display.flip()
        if STRIP:
            strip.show()

########## Margo ######
def margo():
    f_list = [f"margo/pixil-frame-{i}.png" for i in range(5)]
    mp = sprite_data(f_list, vec2(0, 0), 250, False)
    start = pg.time.get_ticks()
    playing = True
    while playing:
        clock.tick(FPS)
        if STRIP:
            clear_strip()
        check_events()
        screen.fill((0, 0, 0))
        mp.draw()
        # if mp.done:
        #     playing = False
        pg.display.flip()
        if STRIP:
            strip.show()
        if pg.time.get_ticks() - start > 5000:
            playing = False

############# DAMIAN
def damian1():
    f_list = ["damian/boo_king_1.png", "damian/boo_king_2.png"]
    mp = sprite_data(f_list, vec2(0, 0), 1500, True)
    sound = pg.mixer.Sound("misc_sounds/king_boo.ogg")
    sound.play()
    start = pg.time.get_ticks()
    playing = True
    while playing:
        clock.tick(FPS)
        if STRIP:
            clear_strip()
        check_events()
        screen.fill((0, 0, 0))
        mp.draw()
        # if mp.done:
        #     playing = False
        pg.display.flip()
        if STRIP:
            strip.show()
        if pg.time.get_ticks() - start > 5000:
            playing = False


def damian2():
    if STRIP:
        clear_strip()
    bow = sprite_data(
        ["damian/ghastly.png"], vec2(0, 0), 250)
    sound = pg.mixer.Sound("misc_sounds/ghastly.mp3")
    sound.play()
    start = pg.time.get_ticks()
    playing = True
    while playing:
        clock.tick(FPS)
        check_events()
        screen.fill((0, 0, 0))
        bow.draw()
        pg.display.flip()
        if STRIP:
            strip.show()
        if pg.time.get_ticks() - start > sound.get_length() * 1000 + 1500:
            playing = False

animation_list = [
    pm_anim1, bowser, creeper, boo_anim, zombie,
    macy_pumpkin, sasha, margo, damian1, damian2
]
shuffle(animation_list)
animations = cycle(animation_list)

while True:
    next(animations)()
    pg.time.wait(2000)  # loop ?
pg.quit()
