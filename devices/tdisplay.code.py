import board
import displayio
import paralleldisplaybus
import adafruit_st7789
import vectorio
import time
import math

displayio.release_displays()

# print(dir(board))

# print("battery", dir(board.BATTERY))

display_bus = paralleldisplaybus.ParallelBus(
    data_pins = (board.LCD_D0, board.LCD_D1, board.LCD_D2, board.LCD_D3,
                 board.LCD_D4, board.LCD_D5, board.LCD_D6, board.LCD_D7),
    command=board.LCD_DC,
    chip_select=board.LCD_CS,
    write=board.LCD_WR,
    read=board.LCD_RD,
    reset=board.LCD_RST,
    frequency = 15_000_000,
)

display = adafruit_st7789.ST7789(display_bus, width=320, height=170, rotation=270, colstart=35)


bg_palette = displayio.Palette(2)
bg_palette[0] = 0xFF00FF
bg_palette[1] = 0x00FF00
bg_rect = vectorio.Rectangle(pixel_shader=bg_palette,
                             width=display.width, height=display.height, x=0, y=0)
display.root_group = displayio.Group()
display.root_group.append(bg_rect)


rects = []
for i in range(25):
    r = vectorio.Rectangle(pixel_shader=bg_palette, width=26,height=5)
    r.color_index = 1
    rects.append(r)
    display.root_group.append(r)


theta = 0.0


display.auto_refresh = True



while True:
    theta += 0.1
    for i,r in enumerate(rects):
        r.x = int(display.width/2) + int(math.sin(theta+i*0.5) * 50)
        r.y = int(display.height/2) + int(math.cos(theta+i*0.5) * 50)
    # time.sleep(0.01)
    display.refresh()
