import gc
import sys
import time

import adafruit_connection_manager
import adafruit_requests
import board
import displayio
import microcontroller
import terminalio
import wifi
from adafruit_button import Button
from adafruit_display_text import label

from custom_terminal_test import Browser
from helper import TDeck

tdeck = TDeck()
display = board.DISPLAY
# pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
# ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)
# requests = adafruit_requests.Session(pool, ssl_context)
COLCOUNT = 50
ROWCOUNT = 15
wifi_params = {
    "pool": adafruit_connection_manager.get_radio_socketpool(wifi.radio),
    "ssl_context": adafruit_connection_manager.get_radio_ssl_context(wifi.radio),
    "requests": adafruit_requests.Session(
        adafruit_connection_manager.get_radio_socketpool(wifi.radio),
        adafruit_connection_manager.get_radio_ssl_context(wifi.radio),
    ),
    "ssid": "JEFF22G",  # You can change this to "JEFF22" if needed
    "password": "Jefferson2022",
}

# Now connect using the correct wifi parameters
wifi.radio.connect(wifi_params["ssid"], wifi_params["password"])
broswer = Browser(displayio, wifi_params)

# Correct the syntax and structure


def wifiM(layout):
    wifiGroup = displayio.Group()
    y_position = 40
    for network in wifi.radio.start_scanning_networks():
        print(f"{network.ssid} [Ch:{network.channel}] RSSI: {network.rssi}")
        wifiLabel = label.Label(
            terminalio.FONT,
            text=network.ssid,
            color=0x000000,
            background_color=0xFFFFFF,
            x=10,
            y=y_position,
        )
        wifiGroup.append(wifiLabel)
        y_position += 30
    display.root_group = wifiGroup


def stats(layout):
    statsGroup = displayio.Group()
    cpu = microcontroller.cpu
    version = sys.version
    used_mem = gc.mem_alloc() / 1024
    free_mem = gc.mem_free() / 1024

    cpuLabel = label.Label(
        terminalio.FONT,
        text=f"CPU: {cpu.frequency / (1 * 1000 * 1000)}mhz",
        color=0x000000,
        background_color=0xFFFFFF,
        padding_left=25,
        padding_right=25,
        padding_top=25,
        padding_bottom=25,
        y=40,
    )
    cpuLabel.x = 10
    statsGroup.append(cpuLabel)
    versionLabel = label.Label(
        terminalio.FONT,
        text=f"Version: {version}",
        color=0x000000,
        background_color=0xFFFFFF,
        padding_left=25,
        padding_right=25,
        padding_top=25,
        padding_bottom=25,
        y=90,
    )
    versionLabel.x = 10
    statsGroup.append(versionLabel)
    usedMemLabel = label.Label(
        terminalio.FONT,
        text=f"Used Mem: {used_mem}k",
        color=0x000000,
        background_color=0xFFFFFF,
        padding_left=25,
        padding_right=25,
        padding_top=25,
        padding_bottom=25,
        y=130,
    )
    usedMemLabel.x = 10
    statsGroup.append(usedMemLabel)
    freeMemLabel = label.Label(
        terminalio.FONT,
        text=f"Free Mem: {free_mem}k",
        color=0x000000,
        background_color=0xFFFFFF,
        padding_left=25,
        padding_right=25,
        padding_top=25,
        padding_bottom=25,
        y=170,
    )
    freeMemLabel.x = 10
    statsGroup.append(freeMemLabel)
    display.root_group = statsGroup


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


def internet(lay):
    broswer.render(
        "https://joshondesign.com/2023/07/25/circuitpython-watch",
    )
    display.root_group = broswer.splash


menu = [
    ["System info", stats],
    ["Exit", exit_menu],
    ["Clock", clock],
    ["Wifi", wifiM],
    ["Internet", internet],
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
