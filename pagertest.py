import board
import terminalio
import displayio
import time
from helper import TDeck

# make some real text
text_nodes = [
    ["Some more plain text that is long and will have to break.","plain"],
    ["Some more plain text that is long and will have to break.","plain"],
    ["Some more plain text that is long and will have to break.","plain"],
    ["Some more plain text that is long and will have to break.","plain"],
    ["A header","header"],
    ["Some more plain text that is long and will have to break.","plain"],
    ["Some more plain text that is long and will have to break.","plain"],
    ["Some more plain text that is long and will have to break.","plain"],
    ["Some more plain text that is long and will have to break.","plain"],
    ["A header","header"],
    ["Some more plain text that is long and will have to break.","plain"],
    ["Some more plain text that is long and will have to break.","plain"],
    ["Some plain text.","plain"],
    ["Some plain text.","plain"],
    ["Some plain text.","plain"],
    ["A header","header"],
    ["A whole bunch of long text that we will need to split.","plain"],
    ["A bold sentence.","bold"],
    ["Some more text.","plain"],
    ["Some more text.","plain"],
    ["A bold word.","bold"],
]



def wrap_text(text, max_width):
    lines = []
    line = []
    current_width = 0
    for chunk in text:
        if current_width + len(chunk[0]) > max_width:
            # print(f"SPLIT: {chunk[0]}")
            words = chunk[0].split()
            before = ""
            for word in words:
                if current_width + len(before) > max_width:
                    # print(f"BREAK at word '{word}'",)
                    line.append([before,chunk[1]])
                    # print("LINE:",line)
                    lines.append(line)
                    line = []
                    before = ""
                    current_width = 0
                before += word + " "
            line.append([before,chunk[1]])
            current_width += len(before)
            continue
        if chunk[1] == 'header':
            # print("LINE:",line)
            lines.append(line)
            lines.append([chunk])
            line = []
            current_width = 0
            continue
        line.append(chunk)
        current_width += len(chunk[0])
        # current_width += 1 # account for spaces
    # print("LINE:",line)
    lines.append(line)
    return lines


output_lines = wrap_text(text_nodes,40)


tdeck = TDeck()
display = board.DISPLAY
splash = displayio.Group()


class HighlightTerminal:
    def __init__(self):
        fontx, fonty = terminalio.FONT.get_bounding_box()
        self.group = displayio.Group()

        plain_palette = displayio.Palette(2)
        plain_palette[0] = 0x000000
        plain_palette[1] = 0x33ff33

        hpal1 = displayio.Palette(2)
        hpal1[0] = 0x000000
        hpal1[1] = 0x0000ff
        hpal1.make_transparent(0)

        hpal2 = displayio.Palette(2)
        hpal2[0] = 0x000000
        hpal2[1] = 0xff0000
        hpal2.make_transparent(0)

        pgrid = displayio.TileGrid(terminalio.FONT.bitmap,
                                        x=0,
                                        y=0,
                                        width=display.width // fontx,
                                        height=display.height // fonty,
                                        tile_width=fontx,
                                        tile_height=fonty,
                                        pixel_shader=plain_palette)
        self.ptermx = terminalio.Terminal(pgrid, terminalio.FONT)
        self.group.append(pgrid)

        hgrid1 = displayio.TileGrid(terminalio.FONT.bitmap,
                                            x=0,
                                            y=0,
                                            width=display.width // fontx,
                                            height=display.height // fonty,
                                            tile_width=fontx,
                                            tile_height=fonty,
                                            pixel_shader=hpal1)
        self.hterm1 = terminalio.Terminal(hgrid1, terminalio.FONT)
        self.group.append(hgrid1)

        hgrid2 = displayio.TileGrid(terminalio.FONT.bitmap,
                                            x=0,
                                            y=0,
                                            width=display.width // fontx,
                                            height=display.height // fonty,
                                            tile_width=fontx,
                                            tile_height=fonty,
                                            pixel_shader=hpal2)
        self.hterm2 = terminalio.Terminal(hgrid2, terminalio.FONT)
        self.group.append(hgrid2)

    def make_spaces(self, txt):
        space = ""
        for i in range(0, len(txt)):
            space += " "
        return space

    def print_plain(self, txt):
        spc = self.make_spaces(txt)
        print(txt, file=self.ptermx, end="")
        print(spc, file=self.hterm1, end="")
        print(spc, file=self.hterm2, end="")

    def print_hl1(self, txt):
        spc = self.make_spaces(txt)
        print(spc, file=self.ptermx, end="")
        print(txt, file=self.hterm1, end="")
        print(spc, file=self.hterm2, end="")

    def print_hl2(self, txt):
        spc = self.make_spaces(txt)
        print(spc, file=self.ptermx, end="")
        print(spc, file=self.hterm1, end="")
        print(txt, file=self.hterm2, end="")

    def print_newline(self):
        print("", file=self.ptermx, end="\r\n")
        print("", file=self.hterm1, end="\r\n")
        print("", file=self.hterm2, end="\r\n")

    def print_line(self, line):
        for sect in line:
            if sect[1] == "header":
                self.print_newline()
                self.print_hl2(sect[0])
                self.print_newline()
            if sect[1] == "link":
                self.print_hl1(sect[0])
            if sect[1] == "bold":
                self.print_hl1(sect[0])
            if sect[1] == 'plain':
                self.print_plain(sect[0])
        self.print_newline()


display.root_group = splash

term = HighlightTerminal()
splash.append(term.group)

for line in output_lines:
    term.print_line(line)

while True:
    keypress = tdeck.get_keypress()
    if keypress:
        print("keypress-", keypress,"-")
        if keypress == ' ':
            print("pressed space")
    # click = tdeck.get_click()
    # if click and click.pressed:
        # popup.perform_selected_item()
    # for p, c in tdeck.get_trackball():
    #     if c > 0:
    #         if p == "right":
                # popup.select_next_item()
            # if p == "left":
                # popup.select_prev_item()
    time.sleep(0.05)  # Simple debounce delay
