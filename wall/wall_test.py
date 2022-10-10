from rpi_ws281x import PixelStrip, Color
import time

## LED MATRIX SETTINGS
LED_COUNT = 400
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False
LED_CHANNEL = 0
ROTATION = 0

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GREY = (75, 75, 75)
BLUE = (84, 88, 213)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
PINK = (255, 193, 204)
CYAN = (0, 255, 255)
ORANGE = (255, 166, 0)
DKBLUE = (3, 79, 254)

colors = [BLACK, WHITE, GREEN, GREY, BLUE, YELLOW, PINK, CYAN, ORANGE, DKBLUE]

strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA,
                    LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

def clear():
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

# for i in range(400):
#     strip.setPixelColor(i, Color(255, 0, 0))
#     strip.show()
#     time.sleep(0.1)
layout = [[i + j * 20 for i in range(20)] for j in range(20)]
for row in range(20):
    if row % 2 == 1:
        layout[row].reverse()
# for row in layout:
#     print(row)

clear()

# for i, c in enumerate(colors):
#     strip.setPixelColor(i, Color(c[0], c[1], c[2]))
#     strip.setPixelColor(i+20, Color(c[1], c[0], c[2]))
# strip.show()
    
# while True:
#     x, y = input("x,y: ").split(",")
#     x, y = int(x), int(y)
#     n = layout[int(y)][int(x)]
#     print(n)
#     strip.setPixelColor(int(n), Color(255, 0, 0))
#     strip.show()

while True:
    r,g,b = input("r,g,b: ").split(",")
    r,g,b = int(r), int(g), int(b)
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(g, r, b))
    strip.show()