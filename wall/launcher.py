import sys
from subprocess import Popen, call
from os import path

running = True
while running:
    call(['python3', "animations.py"])
    call(['python3', "pacman.py"])
