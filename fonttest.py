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
font_w, font_h = terminalio.FONT.get_bounding_box()
print("font size is ", font_w, font_h)

bitmap = displayio.Bitmap(font_w*4,font_h*3,4)
palette = displayio.Palette(4)
palette[0] = 0x000000
palette[1] = 0xFFFFFF
palette[2] = 0xFF0000
palette[3] = 0x0000FF

def draw_letter(bitmap, letter, font, xo, yo, color):
    glyph = font.get_glyph(ord(letter))
    # print("glyph is ", glyph)
    for i in range(0, glyph.width):
        for j in range (0, glyph.height):
            pixel = glyph.bitmap[i + glyph.tile_index*glyph.width,j]
            if pixel == 1:
                pixel = color
            bitmap[i+xo,j+yo] = pixel

for n, ch in enumerate(" ABC"):
    print("ch is ", n, ch)
    draw_letter(bitmap, ch, terminalio.FONT, n * font_w, 0 * font_h, 1)
    draw_letter(bitmap, ch, terminalio.FONT, n * font_w, 1 * font_h, 2)
    draw_letter(bitmap, ch, terminalio.FONT, n * font_w, 2 * font_h, 3)
# draw_letter(bitmap,'B',terminalio.FONT, 1*font_w,0*font_h,1)
# draw_letter(bitmap,'C',terminalio.FONT, 2*font_w,0*font_h,1)


group = displayio.Group()
group.x = 120
group.y = 120
tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette, tile_width=font_w, tile_height=font_h, width=font_w*10, height=font_h*5)
print("ord of A is", ord('A'))
tile_grid[0,0] = 1 # A
tile_grid[1,0] = 3 # C
tile_grid[2,0] = 2 # B
tile_grid[0,1] = 1 + 4 # A in red
tile_grid[0,2] = 1 + 4+4 # A in blue

group.append(tile_grid)
group.scale = 2
display.root_group = group
while True:
    # for x in range(0,bitmap.width):
    #     for y in range(0, bitmap.height):
    #         bitmap[x,y] = 0
    #         if x % 2 == 0:
    #             bitmap[x,y] = 1
    #         if x % 3 == 0:
    #             bitmap[x,y] = 2
    # display.refresh()
    # time.sleep(1)
    display.refresh()
    time.sleep(5)
    # print("====")
