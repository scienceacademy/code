from PIL import Image
from itertools import cycle
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
