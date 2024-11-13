import board
import sys
# import platform
import time
import terminalio
import gc
import microcontroller
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


def print_free_memory():
    print(f"used mem: {gc.mem_alloc()/1024}k")
    print(f"free mem: {gc.mem_free()/1024}k")

def print_platform():
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

def cpu_info():
    cpu = microcontroller.cpu
    print("cpu is", cpu.frequency/(1*1000*1000),"mhz", f"{cpu.temperature}C", cpu.uid, cpu.voltage)

menu = [
    ['free RAM', print_free_memory],
    ['system info', print_platform],
    ['CPU Info', cpu_info],
    ]


line_height = 12 + 5 + 5
layout = GridLayout(
    x=10,
    y=10,
    width=100,
    height=3*line_height,
    grid_size=(1, 3),
    cell_padding=5,
    divider_lines=True,

)
_labels = []

for i in range(0,len(menu)):
    lab = label.Label(terminalio.FONT,
                      text=menu[i][0],
                      color=0x000000,
                      background_color=0xFFFFFF,
                      padding_left= 5,
                      padding_right=5,
                      padding_top=5,
                      padding_bottom=5,
                      )
    _labels.append(lab)
    layout.add_content(lab, grid_position=(0, i), cell_size=(1, 1))

layout.layout_cells()
display.root_group = layout

selected = 0
while True:
    keypress = tdeck.get_keypress()
    if keypress:
        print("keypress-", keypress,"-")
    click = tdeck.get_click()
    if click and click.pressed:
        print("doing",menu[selected][1])
        menu[selected][1]()
    for p, c in tdeck.get_trackball():
        if c > 0:
            # print(f"{p}: {c}")
            layout.get_cell((0,selected)).background_color = 0xFFFFFF
            layout.get_cell((0,selected)).color = 0x000000
            if p == "right":
                selected += 1
                if selected >= len(_labels):
                    selected = 0
            if p == "left":
                selected -= 1
                if selected < 0:
                    selected = len(_labels) -1
            layout.get_cell((0,selected)).background_color = 0x0000FF
            layout.get_cell((0,selected)).color = 0xffffff
    time.sleep(0.05)  # Simple debounce delay



#
