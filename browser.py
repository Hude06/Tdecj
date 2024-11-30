from parser import HtmlParser
import terminalio
import time
import sys

from line_breaker import LineBreaker
import displayio

COLCOUNT = 30


DEBUG = True
def dprint(*args, **kwargs):
    if DEBUG:
        print(*args, file=sys.stderr, **kwargs)

class Browser:
    def __init__(self, wifi_params, display, cols=30, page_size=10):
        self.term = PagingTerminal(display)
        self.overlay = PagingTerminal(display)
        self.parser = HtmlParser()
        self.text_lines = []
        self.output_lines = []
        self.splash = displayio.Group()
        self.splash.append(self.term.grid)
        self.wifi_params = wifi_params
        self.text_url = ""
        self.selected_link_index = 0
        self.links = []
        self.display = display
        self.current_line = -1
        self.page_size = page_size
        self.cols = cols
        dprint("init browser")

    def to_str(self, line):
        dprint("to_str", line)
        ln = ""
        if len(line) < 1:
            dprint("bad line", line)
            return "bad line"

        type = line[0]
        if type == "blank":
            return ""
        if type == "header":
            ln += "## "
        for span in line[1:]:
            ln = ln + span[1]

        # if span[1] == "link":
        #     if self.selected_link_index >= 0:
        #         if span == self.links[self.selected_link_index]:
        #             print("this is the selected link")
        #             ln += " **" + span[0] + "**"
        #             continue
        # ln += line[0]
        return ln

    def load_url(self, url):
        self.term.clear()
        self.overlay.clear()
        self.overlay.render_row(0, "loading: " + url)
        time.sleep(0.1)
        self.text_url = url
        try:
            dprint("Connected to", self.wifi_params["ssid"])
            dprint("fetching", self.text_url)
            with self.wifi_params["requests"].get(self.text_url) as response:
                dprint("loaded bytes", len(response.text))
                self.render_html(response.text)
        except OSError as e:
            dprint("Failed to load", url)
            self.overlay.render_row(0, "Failed to load: " + url)
            return

    def load_file(self, filename):
        self.overlay.clear()
        self.overlay.render_row(0, "loading: " + filename)
        self.text_url = filename
        try:
            with open(filename, "r") as txt:
                self.render_html(txt.read())
        except OSError as e:
            dprint("Failed to load", filename)
            self.overlay.render_row(0, "Failed to load: " + filename)

    def render_html(self, html):
        dprint("rendering", len(html), "bytes")
        lb = LineBreaker()
        count = 0
        for chunk in self.parser.parse(html):
            dprint("got a chunk",chunk)
            count += 1
            if count > 500:
                dprint("done with chunks")
                break
            for line in lb.wrap_text2([chunk],self.cols):
                dprint("line is",line)
                self.output_lines.append(line)
            self.redraw_text()
            self.display.refresh()
            time.sleep(0)
        dprint("done with chunks")
        # track all links
        for line in self.output_lines:
            print("final line is",line)
            if len(line) > 0:
                for span in line:
                    if span[1] == "link":
                        print('we need to track this link',span)
                        self.links.append(span)
        self.redraw_text()
        self.display.refresh()

    # convert lines and spans to rows of plain text for the pager
    def redraw_text(self):
        self.text_lines.clear()
        for line in self.output_lines:
            self.text_lines.append(self.to_str(line))
        self.overlay.render_row(0, "loaded: "+self.text_url)
        if self.current_line + self.page_size >= len(self.text_lines):
            self.current_line = len(self.text_lines) - self.page_size - 1
        if self.current_line < 0:
            self.current_line = 0
        # dprint("doing", self.current_line, 'to ', self.current_line+self.page_size)
        for i in range(0, self.page_size):
            line = ""
            if not self.current_line + i > len(self.text_lines)-1:
                line = self.text_lines[self.current_line+i]
            # dprint("line",line)
            self.term.render_row(i+2,line)
        self.overlay.render_row(self.page_size+3, f"links j = next, k=prev, g=load, lines={len(self.output_lines)}")

    def nav_next_link(self):
        self.selected_link_index += 1
        if self.selected_link_index >= len(self.links):
            self.selected_link_index = 0
        dprint("nav next link", self.links[self.selected_link_index])
        self.redraw_text()

    def nav_prev_link(self):
        self.selected_link_index -= 1
        if self.selected_link_index < 0:
            self.selected_link_index = len(self.links) - 1
        dprint("nav prev link", self.links[self.selected_link_index])
        self.redraw_text()

    def load_selected_link(self):
        link = self.links[self.selected_link_index]
        self.load_url(link[2]['href'])

    def page_down(self):
        self.current_line += self.page_size
        self.redraw_text()


class PagingTerminal:
    def __init__(self, display):
        # self.rows = []
        self.display = display
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
            width=self.display.width // font_w,
            # width=40,
            height=self.display.height // font_h,
            # height=10,
            tile_width=font_w,
            tile_height=font_h,
            pixel_shader=plain_palette,
        )

    def render_row(self, row, line):
        for i in range(0, self.grid.width):
            ch = " "
            if i < len(line):
                ch = line[i]
            glyph = self.font.get_glyph(ord(ch))
            if glyph and glyph.tile_index != None:
                self.grid[i, row] = glyph.tile_index

    # def render_screen(self):
    #     for j in range(0, self.grid.height):
    #         for i in range(0, self.grid.width):
    #             line = ""
    #             if self.current_row + j < len(self.rows):
    #                 line = self.rows[self.current_row + j]
    #             ch = " "
    #             if i < len(line):
    #                 ch = line[i]
    #             glyph = self.font.get_glyph(ord(ch))
    #             if glyph and glyph.tile_index != None:
    #                 self.grid[i, j] = glyph.tile_index

    # def scroll_down(self, amount):
    #     self.current_row += amount
    #     if self.current_row < 0:
    #         self.current_row = 0
    #     self.render_screen()
    #
    # def scroll_top(self):
    #     self.current_row = 0
    #     self.render_screen()

    def clear(self):
        space = self.font.get_glyph(ord(' '))
        for j in range(0, self.grid.height):
            for i in range(0, self.grid.width):
                self.grid[i, j] = space.tile_index


