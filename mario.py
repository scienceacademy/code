from random import choice, random
import pygame as pg
vec2 = pg.Vector2
from itertools import cycle
WIDTH = 600
HEIGHT = 600
PIXEL = 30
FPS = 12
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

def draw_pixel(x, y, col):
    r = pg.Rect(x * PIXEL, y * PIXEL, PIXEL, PIXEL)
    pg.draw.rect(screen, col, r, border_radius=10)
    # pg.draw.circle(screen, col, (x * PIXEL + PIXEL/2,
    #                y * PIXEL + PIXEL/2), PIXEL/2 * 0.9)

class Player:
    def __init__(self):
        self.color = (255, 0, 0)
        self.pos = vec2(0, 17)
        self.gravity = 1
        self.vel = vec2(0, 0)
        self.alive = True

    def update(self):
        if not self.alive:
            return
        self.vel.y += self.gravity
        self.vel.x = 0
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT]:
            self.vel.x += 1
        if keys[pg.K_LEFT]:
            self.vel.x -= 1
        for i in range(int(abs(self.vel.x))):
            self.pos.x += self.vel.x/abs(self.vel.x)
            if map.data[int(self.pos.y)][int(self.pos.x)] != "0":
                self.pos.x -= self.vel.x/abs(self.vel.x)
                self.vel.x = 0
                break
        for i in range(int(abs(self.vel.y))):
            self.pos.y += self.vel.y/abs(self.vel.y)
            if map.data[int(self.pos.y)][int(self.pos.x)] != "0":
                self.pos.y -= self.vel.y/abs(self.vel.y)
                self.vel.y = 0
                break

    def floor_below(self):
        if map.data[int(self.pos.y + 1)][int(self.pos.x)] == "x":
            self.alive = False
        return map.data[int(self.pos.y + 1)][int(self.pos.x)] != "0"

    def jump(self):
        if self.floor_below():
            self.vel.y = -4

    def draw(self, offset):
        draw_pixel(self.pos.x+offset.x, self.pos.y+offset.y, self.color)

class Camera:
    def __init__(self):
        self.camera = pg.Rect(0, 0, map.width, map.height)
        self.width = map.width
        self.height = map.height

    def update(self, target):
        x = -target.pos.x + (WIDTH // PIXEL) // 2
        y = 0
        x = min(0, x)
        x = max(-(self.width - WIDTH // PIXEL - 1), x)
        self.camera = pg.Rect(x, y, self.width, self.height)

map_colors = {
    "1": (222, 89, 24), #bricks
    "q": (255, 193, 124), #? blocks
    "p": (61, 184, 0), #pipe
    "0": (161, 173, 255), #sky
    "b": (252, 188, 176), #cubes
    "x": (0, 0, 0) #placeholder
}
class Map:
    def __init__(self):
        self.data = []
        with open("mario1-1.txt") as f:
            for line in f:
                self.data.append(line.strip())
        self.width = len(self.data[0])
        self.height = len(self.data)
        print(self.width, self.height)

    def draw(self, offset):
        for x in range(WIDTH // PIXEL):
            for y in range(self.height):
                draw_pixel(x, y, map_colors[self.data[int(y-offset.y)][int(x-offset.x)]])


# player movement, jumping
# death
# camera
# coin anim
# grow/shroom?
# goombas
# sounds

map = Map()
cam = Camera()
mario = Player()

playing = True
while playing:
    clock.tick(FPS)
    # get input
    for event in pg.event.get():
        if event.type == pg.QUIT:
            playing = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                mario.jump()
    # update
    mario.update()
    cam.update(mario)

    # update screen
    screen.fill((0, 0, 0))

    map.draw(vec2(cam.camera.topleft))
    mario.draw(vec2(cam.camera.topleft))
    pg.display.flip()

pg.quit()
