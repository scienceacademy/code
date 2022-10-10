from rpi_ws281x import PixelStrip, Color

layout = [[i + j * 20 for i in range(20)] for j in range(20)]
for row in range(20):
    if row % 2 == 1:
        layout[row].reverse()
# for row in layout:
#     print(row)

## LED MATRIX SETTINGS
LED_COUNT = 400
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False
LED_CHANNEL = 0
ROTATION = 0

strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA,
                    LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

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
        print(x, y, n)
        n = 1
    c = Color(col[1], col[0], col[2])
    strip.setPixelColor(int(n), c)