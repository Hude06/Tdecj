from adafruit_displayio_layout.layouts.grid_layout import GridLayout
import terminalio
from adafruit_display_text import label

class PopupMenu:
    def __init__(self, items):
        line_height = 12 + 5 + 5
        self.items = items
        self.selected = 0
        count = len(items)
        print(f"{count} menu items")
        self.selected_color = 0xFFFFFF
        self.layout = GridLayout(
            x=10,
            y=10,
            width=200,
            height= count * line_height,
            grid_size=(1, count),
            cell_padding=5,
            divider_lines=False,
        )
        for i in range(0, len(items)):
            lab = label.Label(
                terminalio.FONT,
                text=items[i][0],
                color=0x000000,
                background_color=0xFFFFFF,
                padding_left=5,
                padding_right=5,
                padding_top=5,
                padding_bottom=5,
            )
            if i == self.selected:
                lab.background_color = 0x0000FF
                lab.color = self.selected_color
            self.layout.add_content(lab, grid_position=(0, i), cell_size=(1, 1))
        self.layout.layout_cells()

    def perform_selected_item(self):
        # print("doing selected item",self.selected,self.items)
        item = self.items[self.selected]
        item[1](item)

    def select_prev_item(self):
        self.layout.get_cell((0, self.selected)).background_color = 0xFFFFFF
        self.layout.get_cell((0, self.selected)).color = 0x000000
        self.selected -= 1
        if self.selected < 0:
            self.selected = len(self.items) - 1
        self.layout.get_cell((0, self.selected)).background_color = 0x0000FF
        self.layout.get_cell((0, self.selected)).color = self.selected_color

    def select_next_item(self):
        self.layout.get_cell((0, self.selected)).background_color = 0xFFFFFF
        self.layout.get_cell((0, self.selected)).color = 0x000000
        self.selected += 1
        if self.selected >= len(self.items):
            self.selected = 0
        self.layout.get_cell((0, self.selected)).background_color = 0x0000FF
        self.layout.get_cell((0, self.selected)).color = 0xFFFFFF
