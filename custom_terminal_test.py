
from parser import HtmlParser

import adafruit_requests
import board
import terminalio
import wifi

from line_breaker import LineBreaker
import displayio

display = board.DISPLAY
COLCOUNT = 50
ROWCOUNT = 15


class Browser:
    def __init__(self, wifi_params):
        self.term = PagingTerminal()
        self.parser = HtmlParser()
        self.text_lines = []
        self.output_lines = []
        self.splash = displayio.Group()
        self.splash.append(self.term.grid)
        self.wifi_params = wifi_params
        self.text_url = ""
        self.selected_link_index = 0
        self.links = []
        print("init browser")

    def to_str(self, line):
        ln = ""
        for span in line:
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

    def load_url(self, url):
        self.text_url = url
        try:
            print("Connected to", self.wifi_params["ssid"])
            print("fetching", self.text_url)
            with self.wifi_params["requests"].get(self.text_url) as response:
                self.render_html(response.text)
        except OSError as e:
            print("Failed to load", url)
            return

    def load_file(self, filename):
        self.text_url = filename
        try:
            with open(filename, "r") as txt:
                self.render_html(txt.read())
        except OSError as e:
            print("Failed to load", filename)

    def render_html(self, html):
        # print("rendering", html)
        chunks = self.parser.parse(html)
        chunks = chunks[0:50]
        # print("chunks", chunks)
        self.output_lines = LineBreaker().wrap_text(chunks, COLCOUNT - 8)
        self.output_lines = self.output_lines[0:100]
        # print("output_lines", self.output_lines)

        # track all links
        for line in self.output_lines:
            if len(line) > 0:
                for span in line:
                    if span[1] == "link":
                        print('we need to track this link',span)
                        self.links.append(span)
        self.redraw_text()

    # convert lines and spans to rows of plain text for the pager
    def redraw_text(self):
        self.text_lines.clear()
        for line in self.output_lines:
            print(line)
            if len(line) > 0:
                self.text_lines.append(self.to_str(line))
        self.term.load_lines(self.text_lines)
        self.term.render_screen()

    def nav_next_link(self):
        self.selected_link_index += 1
        if self.selected_link_index >= len(self.links):
            self.selected_link_index = 0
        print("nav next link", self.links[self.selected_link_index])
        self.redraw_text()

    def nav_prev_link(self):
        self.selected_link_index -= 1
        if self.selected_link_index < 0:
            self.selected_link_index = len(self.links) - 1
        print("nav prev link", self.links[self.selected_link_index])

    def load_selected_link(self):
        link = self.links[self.selected_link_index]
        print("loading link", link)
        self.load_url(link[2]['href'])

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


