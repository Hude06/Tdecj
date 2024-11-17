import time

from browser import Browser
from parser import HtmlParser

import adafruit_connection_manager
import adafruit_requests
import board
import displayio
import terminalio
import wifi

from helper import TDeck

# init tdeck
tdeck = TDeck()
display = board.DISPLAY
splash = displayio.Group()
display.root_group = splash

COLCOUNT = 50
ROWCOUNT = 15

# init highlighter
wifi_params = {
    "pool": adafruit_connection_manager.get_radio_socketpool(wifi.radio),
    "ssl_context": adafruit_connection_manager.get_radio_ssl_context(wifi.radio),
    "requests": adafruit_requests.Session(
        adafruit_connection_manager.get_radio_socketpool(wifi.radio),
        adafruit_connection_manager.get_radio_ssl_context(wifi.radio),
    ),
    "ssid": "JEFF22G",  # You can change this to "JEFF22" if needed
    "password": "Jefferson2022",
}

# Now connect using the correct wifi parameters
wifi.radio.connect(wifi_params["ssid"], wifi_params["password"])
browser = Browser(wifi_params)
display.root_group = browser.splash
# browser.load_url("https://joshondesign.com/2023/07/25/circuitpython-watch")
browser.load_file("links.html")
# handle input events
while True:
    time.sleep(0.01)
    keypress = tdeck.get_keypress()
    if keypress:
        print("keypressss-", keypress, "-")
        if keypress == ' ':
            browser.term.scroll_down(10)
        if keypress == 'j':
            browser.nav_next_link()
        if keypress == 'k':
            browser.nav_prev_link()
        if keypress == 'g':
            browser.load_selected_link()

