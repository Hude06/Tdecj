import time
from parser import HtmlParser

import adafruit_connection_manager
import adafruit_requests
import board
import displayio
import terminalio
import wifi

from helper import TDeck
from line_breaker import LineBreaker

# tdeck = TDeck()
display = board.DISPLAY
# display.root_group = splash
COLCOUNT = 50
ROWCOUNT = 15


def init_lines():
    some_lines = []
    for i in range(150):
        some_lines.append(f"row {i} has some text. some more and longer text too")
    return some_lines


class Browser:
    def __init__(self, displayio, wifi_params):
        self.term = PagingTerminal()
        self.parser = HtmlParser()
        self.lines = []
        self.splash = displayio.Group()
        self.wifi_params = wifi_params
        self.text_url = ""
        self.selected_link_index = 0
        self.links = []
        print("init browser")

    def to_str(self, line):
        ln = ""
        for span in line:
            # print("span is",span)
            if span[1] == "header":
                ln += "## " + span[0]
                continue
            if span[1] == "link":
                if self.selected_link_index >= 0:
                    if span == self.links[self.selected_link_index]:
                        print("this is the selected link")
                        ln += " **" + span[0] + "**"
                        continue
            ln += span[0]
        return ln

    def fetch_url(self, url):
        # Initalize Wifi, Socket Pool, Request Session
        print("initting wifi objects")

        # TEXT_URL = "https://joshondesign.com/c/writings"
        self.text_url = url
        try:
            print("Connected to", self.wifi_params["ssid"])
            print("fetching", self.text_url)
            with self.wifi_params["requests"].get(self.text_url) as response:
                return response.text
        except OSError as e:
            print("Failed to connect to", self.wifi_params["ssid"], e)
            return

    def fetch_file(self, filename):
        with open(filename, "r") as txt:
            return txt.read()

    def render(self, url):
        print("rendering", url)
        # html = self.fetch_url(url)
        html = self.fetch_file("links.html")
        chunks = self.parser.parse(html)
        slice = chunks[0:50]
        output_lines = LineBreaker().wrap_text(slice, COLCOUNT - 8)
        output_lines = output_lines[0:100]
        self.splash.append(self.term.grid)

        # convert lines and spans to rows of plain text for the pager
        for line in output_lines:
            print(line)
            if len(line) > 0:
                for span in line:
                    # print("span",span)
                    if span[1] == "link":
                        print('we need to track this link',span)
                        self.links.append(span)
                if line[0][1] == "header":
                    self.lines.append(" ")
                self.lines.append(self.to_str(line))
                if line[0][1] == "header":
                    self.lines.append(" ")
        self.term.load_lines(self.lines)
        self.term.render_screen()

    def nav_next_link(self):
        print("nav next link", self.links[self.selected_link_index])

    def nav_prev_link(self):
        print("nav prev link", self.links[self.selected_link_index])

class PagingTerminal:
    def __init__(self):
        self.rows = []
        self.current_row = 0
        self.font = terminalio.FONT
        font_w, font_h = terminalio.FONT.get_bounding_box()
        plain_palette = displayio.Palette(2)
        plain_palette[0] = 0x000000
        plain_palette[1] = 0x33FF33

        self.grid = displayio.TileGrid(
            terminalio.FONT.bitmap,
            x=0,
            y=0,
            width=display.width // font_w,
            # width=40,
            height=display.height // font_h,
            # height=10,
            tile_width=font_w,
            tile_height=font_h,
            pixel_shader=plain_palette,
        )

    def load_lines(self, rows):
        self.rows = rows

    def render_screen(self):
        for j in range(0, self.grid.height):
            for i in range(0, self.grid.width):
                line = ""
                if self.current_row + j < len(self.rows):
                    line = self.rows[self.current_row + j]
                ch = " "
                if i < len(line):
                    ch = line[i]
                glyph = self.font.get_glyph(ord(ch))
                if glyph and glyph.tile_index != None:
                    self.grid[i, j] = glyph.tile_index

    def scroll_down(self, amount):
        self.current_row += amount
        if self.current_row < 0:
            self.current_row = 0
        self.render_screen()

    def scroll_top(self):
        self.current_row = 0
        self.render_screen()




# html = fetch_url()
# parser = HtmlParser()
# chunks = parser.parse(html)
# slice = chunks[0:50]
# print("==== chunks ====")
# # for chunk in slice:
# #     print(chunk)
# output_lines = LineBreaker().wrap_text(slice, COLCOUNT - 8)
# output_lines = output_lines[0:100]
# print(f"==== output lines ==== {len(output_lines)}")

# add extra lines between headers

# while True:
#     time.sleep(0.01)
#     keypress = tdeck.get_keypress()
#     if keypress:
#         print("keypress-", keypress, "-")
#         if keypress == ' ':
#             broswer.term.scroll_down(10)
#         if keypress == 't':
#             broswer.term.scroll_top()
#         if keypress == 'j':
#             broswer.term.scroll_down(1)
#         if keypress == 'k':
#             broswer.term.scroll_down(-1)
