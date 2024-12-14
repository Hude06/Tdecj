import gc
import sys

# import platform
import time

import board
import busio
import digitalio
import displayio
import microcontroller
import terminalio
from adafruit_button import Button
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
from adafruit_displayio_layout.layouts.grid_layout import GridLayout

import helper
from helper import TDeck
from popupmenu import PopupMenu

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
    # print("platform is", platform.platform())
    # print("python compiler is", platform.python_compiler())
    # print("libc ver is", platform.libc_ver())


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
    print("exiting")


menu = [
    ["Free RAM", print_free_memory],
    ["System info", print_platform],
    ["CPU Info", cpu_info],
    ["Exit", exit_menu],
]




popup = PopupMenu(menu)
display.root_group = popup.layout

while True:
    keypress = tdeck.get_keypress()
    if keypress:
        print("keypress-", keypress, "-")
        if keypress == " ":
            popup.layout.hidden = False
    click = tdeck.get_click()
    if click and click.pressed:
        popup.perform_selected_item()
    for p, c in tdeck.get_trackball():
        if c > 0:
            if p == "right":
                popup.select_next_item()
            if p == "down":
                popup.select_next_item()
            if p == "left":
                popup.select_prev_item()
            if p == "up":
                popup.select_prev_item()
    time.sleep(0.05)  # Simple debounce delay


#
