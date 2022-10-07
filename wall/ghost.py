import time

from rpi_ws281x import ws, Color, Adafruit_NeoPixel
LED_COUNT = 400        # Number of LED pixels.
LED_PIN = 18
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
# DMA channel to use for generating signal (Between 1 and 14)
LED_DMA = 10
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
# True to invert the signal (when using NPN transistor level shift)
LED_INVERT = False
LED_CHANNEL = 0       # 0 or 1
LED_STRIP = ws.SK6812_STRIP_GRBW

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ,
                           LED_DMA, LED_INVERT, LED_BRIGHTNESS,
                           LED_CHANNEL, LED_STRIP)

