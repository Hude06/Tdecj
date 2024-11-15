import audiobusio
import audiocore
import board
import array
import time
import math

from helper import TDeck

tdeck = TDeck()

while True:
    time.sleep(0.01)
    keypress = tdeck.get_keypress()
    if keypress:
        print(f"keypress '{keypress}' {ord(keypress)}")
    for p, c in tdeck.get_trackball():
        if c > 0:
            print(f"trackball {p}: {c}")


