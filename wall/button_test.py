import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

button1 = 24

GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_UP)

last = False
while True:
    state1 = GPIO.input(button1)
    if last != state1: 
        print(state1)
    last = state1
    time.sleep(0.05)
