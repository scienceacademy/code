import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

buttons = {
    16: "pg.K_UP",
    18: "pg.K_RIGHT",
    13: "pg.K_LEFT",
    15: "pg.K_DOWN"
}

for butt in buttons:
    GPIO.setup(butt, GPIO.IN, pull_up_down=GPIO.PUD_UP)

last = False
while True:
    for butt in buttons:
        state = GPIO.input(butt)
        if state == 0:
           print(butt)
    time.sleep(0.05)
