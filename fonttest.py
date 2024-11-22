import time
import terminalio
import displayio
from waveshare128 import setup_display
display = setup_display()

# - [ ] Copy font glyph into another bitmap with a different palette. Palette remapping
# - [ ] `bmpB[x, y] = some_function(bmpA[x, y])`
# - [ ] https://learn.adafruit.com/circuitpython-display-support-using-displayio/bitmap-and-palette
# - [ ] Get the glyph for the letter A.
# - [ ] Get bitmap coords for the glyph
# - [ ] Create new bitmap big enough for two letters
# - [ ] Set palette to four colors
# - [ ] Copy letter A to bitmap one pixel at a time
# - [ ] Copy a second time with a different color

font = terminalio.FONT
# print("font size is ", font_w, font_h)


palette = displayio.Palette(4)
palette[0] = 0x000000
palette[1] = 0xFFFFFF
palette[2] = 0xFF0000
palette[3] = 0x0000FF

class MulticolorTextGrid:
    def __init__(self, rows, cols, font, palette):
        self.rows = rows
        self.cols = cols
        self.font = font
        font_w, font_h = self.font.get_bounding_box()
        print("font bitmap size", self.font.bitmap.width, self.font.bitmap.height)
        self.font_w = font_w
        self.font_h = font_h
        self.palette = palette
        self.base_text = " ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.bitmap = displayio.Bitmap(self.font_w*len(self.base_text),
                                       self.font_h*len(palette),
                                       len(palette))
        print("new bitmap size ", self.bitmap.width, self.bitmap.height)
        self.tile_grid = displayio.TileGrid(self.bitmap,
                                            pixel_shader=palette,
                                            tile_width=font_w,
                                            tile_height=font_h,
                                            width=font_w*10,
                                            height=font_h*5)

        for n, ch in enumerate(self.base_text):
            for i in range(len(palette)-1):
                self.draw_letter(ch, n * font_w, i * font_h, i+1)

    def draw_letter(self, letter, xo, yo, color):
        # print("stamping ", letter, 'at',xo,yo,'in color',color)
        glyph = self.font.get_glyph(ord(letter))
        for i in range(0, glyph.width):
            for j in range (0, glyph.height):
                pixel = glyph.bitmap[i + glyph.tile_index * glyph.width,j]
                if pixel == 1:
                    pixel = color
                self.bitmap[i+xo,j+yo] = pixel

    def set_text(self, x, y, text, color):
        for n, ch in enumerate(text):
            fx = x + n
            # print(ch, ord(ch),'x',x,n,fx)
            if fx < self.cols:
                self.tile_grid[fx,y] = ord(ch) - 65 + 1 + len(self.base_text) * color


group = displayio.Group()
group.x = 120
group.y = 120

text_grid = MulticolorTextGrid(4,10,terminalio.FONT, palette)
text_grid.set_text(0,0,"ABC",1)
text_grid.set_text(3,0,"ABC",2)
text_grid.set_text(6,0,"ABC",0)
group.append(text_grid.tile_grid)
group.scale = 2
display.root_group = group
while True:
    display.refresh()
    time.sleep(5)
    # print("====")
