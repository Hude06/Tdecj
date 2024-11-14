import board
import terminalio
import displayio
import time

class HighlightTerminal:
    def __init__(self, rowcount, colcount):
        x = 0
        y = 0
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
                                   x=x,
                                   y=y,
                                   # width=display.width // fontx,
                                   width=colcount,
                                   # height=display.height // fonty,
                                   height=rowcount,
                                   tile_width=fontx,
                                   tile_height=fonty,
                                   pixel_shader=plain_palette)
        self.ptermx = terminalio.Terminal(pgrid, terminalio.FONT)
        self.group.append(pgrid)

        hgrid1 = displayio.TileGrid(terminalio.FONT.bitmap,
                                    x=x,
                                    y=y,
                                    width=colcount,
                                    height=rowcount,
                                    tile_width=fontx,
                                    tile_height=fonty,
                                    pixel_shader=hpal1)
        self.hterm1 = terminalio.Terminal(hgrid1, terminalio.FONT)
        self.group.append(hgrid1)

        hgrid2 = displayio.TileGrid(terminalio.FONT.bitmap,
                                    x=x,
                                    y=y,
                                    width=colcount,
                                    height=rowcount,
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
