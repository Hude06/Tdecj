import board
import time
import re
import terminalio
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
import displayio
from adafruit_button import Button
import digitalio
import busio
import helper
from helper import TDeck
# from sx1262 import SX1262
import time
import wifi
from adafruit_displayio_layout.layouts.grid_layout import GridLayout
import adafruit_connection_manager
import adafruit_requests
import parser

print(dir(board))
# sx = SX1262(spi_bus=board.SPI, clk=board.SCK, mosi=board.MOSI, miso=board.MISO, cs=board.LORA_CS, irq=20, rst=board.LORA_RST, gpio=2)

# LoRa
# sx.begin(freq=923, bw=500.0, sf=12, cr=8, syncWord=0x12,
#          power=-5, currentLimit=60.0, preambleLength=8,
#          implicit=False, implicitLen=0xFF,
#          crcOn=True, txIq=False, rxIq=False,
#          tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)

# FSK
##sx.beginFSK(freq=923, br=48.0, freqDev=50.0, rxBw=156.2, power=-5, currentLimit=60.0,
##            preambleLength=16, dataShaping=0.5, syncWord=[0x2D, 0x01], syncBitsLength=16,
##            addrFilter=SX126X_GFSK_ADDRESS_FILT_OFF, addr=0x00, crcLength=2, crcInitial=0x1D0F, crcPolynomial=0x1021,
##            crcInverted=True, whiteningOn=True, whiteningInitial=0x0100,
##            fixedPacketLength=False, packetLength=0xFF, preambleDetectorLength=SX126X_GFSK_PREAMBLE_DETECT_16,
##            tcxoVoltage=1.6, useRegulatorLDO=False,
##            blocking=True)

# while True:
#     msg, err = sx.recv()
#     if len(msg) > 0:
#         error = SX1262.STATUS[err]
#         print(msg)
#         print(error)


# # Initialize the T-Deck
tdeck = TDeck()

# # Set up the display
display = board.DISPLAY

# TRACKBALL_SCALE = 10

## scan for wifi


# layout = GridLayout(
#     x=10,
#     y=10,
#     width=200,
#     height=200,
#     grid_size=(1, 15),
#     cell_padding=2,
# )    

# _labels = []

# print ("Broadcasted SSIDs")
# count = 0
# for network in wifi.radio.start_scanning_networks():
#     print(f"{network.ssid} [Ch:{network.channel}] RSSI: {network.rssi}")
#     lab = label.Label(terminalio.FONT, text=network.ssid, color=0x000000, background_color=0xFFFFFF)
#     _labels.append(lab)
#     layout.add_content(lab, grid_position=(0, count), cell_size=(1, 1))
#     count += 1



# display.root_group = layout

# selected = 0

# Initalize Wifi, Socket Pool, Request Session
pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)
requests = adafruit_requests.Session(pool, ssl_context)


def fetch_url(logterm):
    ssid = "JEFF22G"
    # ssid = "JEFF22"
    password = "Jefferson2022"
    # TEXT_URL = "https://joshondesign.com/c/writings"
    TEXT_URL = "https://joshondesign.com/2023/07/25/circuitpython-watch"
    try:
        wifi.radio.connect(ssid, password)
        print("Connected to", ssid)
        with requests.get(TEXT_URL) as response:
            # print(response.text)
            print("got the page")
            chunks = parser.process_html(response.text)
            for chunk in chunks:
                if chunk[0] == 'h3':
                    print("\n### ", chunk[1],"\n")
                    continue
                if chunk[0] == 'h2':
                    print("\n## ", chunk[1],"\n")
                    continue
                if chunk[0] == 'h1':
                    print("\n# ", chunk[1],"\n")
                    continue
                if chunk[0] == 'li':
                    print("* ", chunk[1])
                    continue
                if chunk[0] == 'plain':
                    print("", chunk[1])
                    continue
                if chunk[0] == 'p':
                    print("", chunk[1],"\n")
                    print("\r\n" + chunk[1], file=logterm, end="")
                    continue
                if chunk[0] == 'a':
                    print("LINK ", chunk[1])
                    print("\r\nLINK!" + chunk[1], file=logterm, end="")
                    continue
                print(chunk)

    except OSError as e:
        print("Failed to connect to", ssid, e)
        return


# # # Main loop
# while True:
#     # Check for click (currently does nothing, just prints)
    # keypress = tdeck.get_keypress()  
    # if keypress:
    #     # print("keypress-", keypress,"-")
    #     # text_area.text = text_area.text + keypress
    #     layout.get_cell((0,selected)).background_color = 0xFFFFFF
    #     if keypress == 'j':
    #         selected += 1
    #         if selected > len(_labels) - 1:
    #             selected = len(_labels) - 1
    #     if keypress == 'k':
    #         selected -= 1
    #         if selected < 0:
    #             selected = 0
    #     if keypress == '\r':
    #         print("pressed enter")
    #         fetch_url()
    #     layout.get_cell((0,selected)).background_color = 0x0000FF




#     for p, c in tdeck.get_trackball():
#         if c > 0:
#             print(f"{p}: {c}")
#             if p == "right":
#                 mouse.x += c*TRACKBALL_SCALE
#             if p == "left":
#                 mouse.x -= c*TRACKBALL_SCALE
#             if p == "up":
#                 mouse.y += c*TRACKBALL_SCALE
#             if p == "down":
#                 mouse.y -= c*TRACKBALL_SCALE
#             # mouse.x += {c}
#             # mouse.y += {p}


 # time.sleep(0.05)  # Simple debounce delay


print("running here")
display = board.DISPLAY  # or equivalent external display library

splash = displayio.Group()

fontx, fonty = terminalio.FONT.get_bounding_box()
term_palette = displayio.Palette(2)
term_palette[0] = 0x000000
term_palette[1] = 0x33ff33
logbox = displayio.TileGrid(terminalio.FONT.bitmap,
                            x=0,
                            y=0,
                            width=display.width // fontx,
                            height=display.height // fonty,
                            tile_width=fontx,
                            tile_height=fonty,
                            pixel_shader=term_palette)
splash.append(logbox)
logterm = terminalio.Terminal(logbox, terminalio.FONT)

display.root_group = splash

# print("Hello Serial!", file=sys.stdout)  # serial console
print("\r\nHello displayio!", file=logterm, end="\r\n")  # displayio

# fetch_url(logterm)

def fetch_disk_html(logterm):
    with open("/test.html","r") as txt:
        html = txt.read()
        print("opened the file",html)
        chunks = parser.process_html(html)
        for chunk in chunks:
            print(re.sub(r"\s",' ',chunk[1]))
            ch = chunk[1].strip()
            if len(ch) > 0:
                if chunk[0] == 'h1':
                    print("### ", file=logterm, end = "")
                print(chunk[1].replace('\n',''), file=logterm, end="\r\n")

fetch_disk_html(logterm)

# print("\033["+"31m"+"Hello Serial!"+"\033["+"0m")  # serial console
# print("\033["+"31m"+"Hello Serial!"+"\033["+"0m", file=logterm)  # serial console
# print("\033[2J", file=logterm)

def clear_screen(logterm):
    print("\033[2J", file=logterm)

# scroll up
# for row in range(10 - 1, 0, -1):
#     for column in range(0, 40):
#         logbox[column, row] = logbox[column, row - 1]

# scroll down
# for row in range(0, 10 - 1):
#     for column in range(0, 40):
#         logbox[column, row] = logbox[column, row + 1]

while True:
    time.sleep(0.01)
    keypress = tdeck.get_keypress()  
    if keypress:
        print("keypress-", keypress,"-")
        # text_area.text = text_area.text + keypress
        # layout.get_cell((0,selected)).background_color = 0xFFFFFF
        # if keypress == 'j':
        # logterm.write("\033[D")
        # print(dir(logterm))
        # scroll_back(logterm)
        # logterm.write("\033[2J")
        # print(dir(logbox))




# print("\r\nmore text", file=logterm, end="")
# parser.process_html("<html><p>hello there</p></html>")

