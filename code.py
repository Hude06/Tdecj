import board
import time
import terminalio
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
import displayio
from adafruit_button import Button
import digitalio
import busio
import helper
from helper import TDeck
from sx1262 import SX1262
import time
import wifi
from adafruit_displayio_layout.layouts.grid_layout import GridLayout
import adafruit_connection_manager
import adafruit_requests

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

layout = GridLayout(
    x=10,
    y=10,
    width=200,
    height=200,
    grid_size=(1, 15),
    cell_padding=2,
)    

_labels = []

print ("Broadcasted SSIDs")
count = 0
for network in wifi.radio.start_scanning_networks():
    print(f"{network.ssid} [Ch:{network.channel}] RSSI: {network.rssi}")
    lab = label.Label(terminalio.FONT, text=network.ssid, color=0x000000, background_color=0xFFFFFF)
    _labels.append(lab)
    layout.add_content(lab, grid_position=(0, count), cell_size=(1, 1))
    count += 1



display.root_group = layout

selected = 0

# Initalize Wifi, Socket Pool, Request Session
pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)
requests = adafruit_requests.Session(pool, ssl_context)
# rssi = wifi.radio.ap_info.rssi

def fetch_url():
    ssid = "JEFF22G"
    password = "Jefferson2022"
    TEXT_URL = "https://joshondesign.com/c/writings"
    try:
        wifi.radio.connect(ssid, password)
        print("Connected to", ssid)
        with requests.get(TEXT_URL) as response:
            print(response.text)

    except OSError as e:
        print("Failed to connect to", ssid, e)
        return


# # # Main loop
while True:
#     # Check for click (currently does nothing, just prints)
    keypress = tdeck.get_keypress()  
    if keypress:
        # print("keypress-", keypress,"-")
        # text_area.text = text_area.text + keypress
        layout.get_cell((0,selected)).background_color = 0xFFFFFF
        if keypress == 'j':
            selected += 1
            if selected > len(_labels) - 1:
                selected = len(_labels) - 1
        if keypress == 'k':
            selected -= 1
            if selected < 0:
                selected = 0
        if keypress == '\r':
            print("pressed enter")
            fetch_url()
        layout.get_cell((0,selected)).background_color = 0x0000FF




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


    time.sleep(0.05)  # Simple debounce delay
