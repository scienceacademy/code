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


strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA,
                    LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

def clear():
    for i in range(400):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

for i in range(400):
    strip.setPixelColor(i, Color(255, 0, 0))
    strip.show()
    time.sleep(0.1)

clear()