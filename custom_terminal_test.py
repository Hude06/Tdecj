import board
import terminalio
import displayio
import time
import wifi
from helper import TDeck
import adafruit_connection_manager
import adafruit_requests

from line_breaker import LineBreaker
from parser import HtmlParser

tdeck = TDeck()
display = board.DISPLAY
splash = displayio.Group()
display.root_group = splash



def init_lines():
    some_lines = []
    for i in range(150):
        some_lines.append(f"row {i} has some text. some more and longer text too")
    return some_lines

# lines = init_lines()

class PagingTerminal:
    def __init__(self):
        self.rows = []
        self.current_row = 0
        self.font = terminalio.FONT
        font_w, font_h = terminalio.FONT.get_bounding_box()
        plain_palette = displayio.Palette(2)
        plain_palette[0] = 0x000000
        plain_palette[1] = 0x33ff33

        self.grid = displayio.TileGrid(terminalio.FONT.bitmap,
                                  x=0, y=0,
                                  width=display.width // font_w,
                                  # width=40,
                                  height=display.height // font_h,
                                  # height=10,
                                  tile_width=font_w,
                                  tile_height=font_h,
                                  pixel_shader=plain_palette
                                  )

    def load_lines(self, rows):
        self.rows = rows

    def render_screen(self):
        for j in range(0,self.grid.height):
            for i in range(0,self.grid.width):
                line = ""
                if self.current_row + j < len(self.rows):
                    line = self.rows[self.current_row + j]
                ch = ' '
                if i < len(line):
                    ch = line[i]
                glyph = self.font.get_glyph(ord(ch))
                if glyph and glyph.tile_index != None:
                    self.grid[i,j] = glyph.tile_index

    def scroll_down(self, amount):
        self.current_row += amount
        if self.current_row < 0:
            self.current_row = 0
        self.render_screen()

    def scroll_top(self):
        self.current_row = 0
        self.render_screen()

def fetch_file():
    with open("blog.html", "r") as txt:
        return txt.read()


COLCOUNT = 50
ROWCOUNT = 15

html = fetch_file()
parser = HtmlParser()
chunks = parser.parse(html)
slice = chunks[0:50]
print("==== chunks ====")
# for chunk in slice:
#     print(chunk)
output_lines = LineBreaker().wrap_text(slice, COLCOUNT - 8)
output_lines = output_lines[0:100]
print(f"==== output lines ==== {len(output_lines)}")

def to_str(line):
    ln = ""
    for span in line:
        # print("span is",span)
        if span[1] == 'header':
            ln += "## " + span[0]
            continue
        ln += span[0]
    return ln

# add extra lines between headers
lines = []
for line in output_lines:
    print(line)
    if len(line) > 0:
        if line[0][1] == 'header':
            lines.append(" ")
        lines.append(to_str(line))
        if line[0][1] == 'header':
            lines.append(" ")

term = PagingTerminal()

splash.append(term.grid)
term.load_lines(lines)
term.render_screen()

while True:
    time.sleep(0.01)
    keypress = tdeck.get_keypress()
    if keypress:
        print("keypress-", keypress, "-")
        if keypress == ' ':
            term.scroll_down(10)
        if keypress == 't':
            term.scroll_top()
        if keypress == 'j':
            term.scroll_down(1)
        if keypress == 'k':
            term.scroll_down(-1)
