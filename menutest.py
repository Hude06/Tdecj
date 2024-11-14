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
    print("cpu is", cpu.frequency/(1*1000*1000),"mhz", f"{cpu.temperature}C", cpu.uid, cpu.voltage)

def exit_menu(lay):
    lay.hidden = True

menu = [
    ['Free RAM', print_free_memory],
    ['System info', print_platform],
    ['CPU Info', cpu_info],
    ['Exit', exit_menu]
    ]


class PopupMenu():
    def __init__(self, items):
        line_height = 12 + 5 + 5
        self.items = items
        self.selected = 0
        self.layout = GridLayout(
            x=10,
            y=10,
            width=100,
            height=4*line_height,
            grid_size=(1, 4),
            cell_padding=5,
            divider_lines=True,
            )
        for i in range(0,len(items)):
            lab = label.Label(terminalio.FONT,
                              text=items[i][0],
                              color=0x000000,
                              background_color=0xFFFFFF,
                              padding_left= 5,
                              padding_right=5,
                              padding_top=5,
                              padding_bottom=5,
                              )
            self.layout.add_content(lab, grid_position=(0, i), cell_size=(1, 1))
        self.layout.layout_cells()

    def perform_selected_item(self):
        self.items[self.selected][1](self.layout)

    def select_prev_item(self):
        self.layout.get_cell((0,self.selected)).background_color = 0xFFFFFF
        self.layout.get_cell((0,self.selected)).color = 0x000000
        self.selected -= 1
        if self.selected < 0:
            self.selected = len(self.items) -1
        self.layout.get_cell((0,self.selected)).background_color = 0x0000FF
        self.layout.get_cell((0,self.selected)).color = 0xffffff

    def select_next_item(self):
        self.layout.get_cell((0,self.selected)).background_color = 0xFFFFFF
        self.layout.get_cell((0,self.selected)).color = 0x000000
        self.selected += 1
        if self.selected >= len(self.items):
            self.selected = 0
        self.layout.get_cell((0,self.selected)).background_color = 0x0000FF
        self.layout.get_cell((0,self.selected)).color = 0xffffff

popup = PopupMenu(menu)
display.root_group = popup.layout

while True:
    keypress = tdeck.get_keypress()
    if keypress:
        print("keypress-", keypress,"-")
        if keypress == ' ':
            popup.layout.hidden = False
    click = tdeck.get_click()
    if click and click.pressed:
        popup.perform_selected_item()
    for p, c in tdeck.get_trackball():
        if c > 0:
            if p == "right":
                popup.select_next_item()
            if p == "left":
                popup.select_prev_item()
    time.sleep(0.05)  # Simple debounce delay



#
