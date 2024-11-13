import board
import time
import terminalio
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
import displayio
from adafruit_button import Button
import digitalio
import busio
import helper
from helper import TDeck
import time
from adafruit_displayio_layout.layouts.grid_layout import GridLayout

tdeck = TDeck()
display = board.DISPLAY
layout = GridLayout(
    x=10,
    y=10,
    width=200,
    height=200,
    grid_size=(1, 15),
    cell_padding=2,
)
_labels = []

for i in range(0,5):
    lab = label.Label(terminalio.FONT, text="hi there", color=0x000000, background_color=0xFFFFFF)
    _labels.append(lab)
    layout.add_content(lab, grid_position=(0, i), cell_size=(1, 1))


display.root_group = layout

selected = 0
while True:
    keypress = tdeck.get_keypress()
    if keypress:
        print("keypress-", keypress,"-")
        # layout.get_cell((0,selected)).background_color = 0xFFFFFF
    for p, c in tdeck.get_trackball():
        if c > 0:
            print(f"{p}: {c}")
            layout.get_cell((0,selected)).background_color = 0xFFFFFF
            if p == "right":
                selected += 1
            if p == "left":
                selected -= 1
            layout.get_cell((0,selected)).background_color = 0x0000FF
    time.sleep(0.05)  # Simple debounce delay



#
