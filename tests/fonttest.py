import time
from math import floor

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
        print("font tile count", self.font.bitmap.width/font_w)
        self.font_w = font_w
        self.font_h = font_h
        self.palette = palette
        self.base_text = " ABC"
        self.bitmap = displayio.Bitmap(self.font.bitmap.width,
                                       self.font.bitmap.height * len(self.palette),
                                       len(self.palette))
        print("new bitmap size ", self.bitmap.width, self.bitmap.height)
        self.tile_grid = displayio.TileGrid(self.bitmap,
                                            pixel_shader=palette,
                                            tile_width=font_w,
                                            tile_height=font_h,
                                            width=font_w*self.cols,
                                            height=font_h*self.rows)
        for i in range(self.font.bitmap.width):
            for j in range(self.font.bitmap.height):
                pixel = self.font.bitmap[i, j]
                if pixel == 1:
                    for c in range(len(self.palette)-1):
                        self.bitmap[i, j + font_h*c] = c+1

    def set_text(self, x, y, text, color):
        tc = floor(self.bitmap.width / self.font_w)
        # print("tc",tc)
        for n, ch in enumerate(text):
            fx = x + n
            # print(ch, ord(ch),'x',x,n,fx)
            if fx < self.cols:
                glyph = self.font.get_glyph(ord(ch))
                # print("glyph",glyph.tile_index,'ch',color*tc)
                self.tile_grid[fx,y] = glyph.tile_index + color*tc

group = displayio.Group()
group.x = 60
group.y = 120

text_grid = MulticolorTextGrid(4,30,terminalio.FONT, palette)
text_grid.set_text(0,0,"Some cool text",0)
text_grid.set_text(15,0,"including",1)
text_grid.set_text(0,1,"red",1)
# text_grid.set_text(4,1,"and blue",2)
text_grid.set_text(0,2,"and back to white",0)

group.append(text_grid.tile_grid)
group.scale = 1
display.root_group = group
while True:
    display.refresh()
    time.sleep(5)
    # print("====")
