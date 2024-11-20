import time
from helper import TDeck

tdeck = TDeck()

print(f"Battery Voltage: {tdeck.get_battery_voltage():.2f} V")

while True:
    time.sleep(0.01)
    keypress = tdeck.get_keypress()
    if keypress:
        print(f"keypress '{keypress}' {ord(keypress)}")
    for p, c in tdeck.get_trackball():
        if c > 0:
            print(f"trackball {p}: {c}")

