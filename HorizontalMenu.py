import gc
import sys
import time

import board
import displayio
import microcontroller
import terminalio
from adafruit_button import Button
from adafruit_display_text import label

from helper import TDeck

tdeck = TDeck()
display = board.DISPLAY


def print_free_memory(layout):
    print(f"used mem: {gc.mem_alloc()/1024}k")
    print(f"free mem: {gc.mem_free()/1024}k")


def print_platform(layout):
    print("byteorder is", sys.byteorder)
    print("impl is", sys.implementation)
    print("maxsize is", sys.maxsize)
    print("version is", sys.version)
    print("version info", sys.version_info)
    print("platform is", sys.platform)
    print("modules is", sys.modules)


def cpu_info(layout):
    cpu = microcontroller.cpu
    print(
        "cpu is",
        cpu.frequency / (1 * 1000 * 1000),
        "mhz",
        f"{cpu.temperature}C",
        cpu.uid,
        cpu.voltage,
    )


def exit_menu(lay):
    lay.hidden = True


def clock(lay):
    print(time.localtime())
    clockGroup = displayio.Group()
    clockLabel = label.Label(
        terminalio.FONT,
        text=str("12:10"),
        color=0x000000,
        background_color=0xFFFFFF,
        padding_left=25,
        padding_right=25,
        padding_top=25,
        padding_bottom=25,
        y=120,
    )
    clockGroup.append(clockLabel)
    display.root_group = clockGroup


menu = [
    ["System info", print_platform],
    ["CPU info", cpu_info],
    ["Exit", exit_menu],
    ["Free RAM", print_free_memory],
    ["Clock", clock],
]


class PopupMenu:
    def __init__(self, items):
        self.items = items
        self.selected = 0
        self.layout = displayio.Group()
        self.labels = []

        for i, item in enumerate(items):
            lab = label.Label(
                terminalio.FONT,
                text=item[0],
                color=0x000000,
                background_color=0xFFFFFF,
                padding_left=25,
                padding_right=25,
                padding_top=25,
                padding_bottom=25,
                y=120,
            )
            lab.x = (
                i * (lab.bounding_box[3] + 125)
            ) + 100  # Adjust the spacing as needed
            self.labels.append(lab)
            self.layout.append(lab)

        self.update_selection()

    def update_selection(self):
        for i, lab in enumerate(self.labels):
            if i == self.selected:
                lab.background_color = 0x0000FF  # Blue for selected item
            else:
                lab.background_color = 0xFFFFFF  # White for non-selected items

    def perform_selected_item(self):
        self.items[self.selected][1](self.layout)

    def select_prev_item(self):
        self.selected -= 1
        if self.selected < 0:
            self.selected = 0
        self.update_selection()
        self.scroll_items()

    def select_next_item(self):
        self.selected += 1
        if self.selected >= len(self.items):
            self.selected = len(self.items) - 1
        self.update_selection()
        self.scroll_items()

    def scroll_items(self):
        # Ensure items wrap properly
        for i, lab in enumerate(self.labels):
            # Adjust `x` positions of the items based on the current selection
            lab.x = (i - self.selected) * (lab.bounding_box[3] + 125) + 100

        # Optionally, add additional logic to make sure the menu doesn't scroll off-screen
        # If the labels exceed the display width, adjust the x position accordingly.


popup = PopupMenu(menu)
display.root_group = popup.layout

while True:
    keypress = tdeck.get_keypress()
    if keypress:
        print("keypress-", keypress, "-")
        if keypress == " ":
            display.root_group = popup.layout
    click = tdeck.get_click()
    if click and click.pressed:
        popup.perform_selected_item()

    for p, c in tdeck.get_trackball():
        if c > 0:
            if p == "right":
                popup.select_next_item()
                time.sleep(0.5)
            if p == "left":
                popup.select_prev_item()
                time.sleep(0.5)
    time.sleep(0.05)  # Simple debounce delay
