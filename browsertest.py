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
from paging_terminal import HighlightTerminal

# init tdeck
tdeck = TDeck()
display = board.DISPLAY
splash = displayio.Group()
display.root_group = splash

COLCOUNT = 50
ROWCOUNT = 15

# init highlighter
term = HighlightTerminal(ROWCOUNT,COLCOUNT)
splash.append(term.group)

term.print_line(["Loading...","plain"])



# fetch the page
def fetch_url():
    # Initalize Wifi, Socket Pool, Request Session
    print("initting wifi objects")
    pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
    ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)
    requests = adafruit_requests.Session(pool, ssl_context)

    ssid = "JEFF22G"
    # ssid = "JEFF22"
    password = "Jefferson2022"
    # TEXT_URL = "https://joshondesign.com/c/writings"
    text_url = "https://joshondesign.com/2023/07/25/circuitpython-watch"
    try:
        print("connecting to", ssid)
        wifi.radio.connect(ssid, password)
        print("Connected to", ssid)
        print("fetching",text_url)
        with requests.get(text_url) as response:
            return response.text
    except OSError as e:
        print("Failed to connect to", ssid, e)
        return

def fetch_file():
    with open("blog.html", "r") as txt:
        return txt.read()

# html = fetch_url()
html = fetch_file()

parser = HtmlParser()
chunks = parser.parse(html)
slice = chunks[0:50]
print("==== chunks ====")
for chunk in slice:
    print(chunk)
output_lines = LineBreaker().wrap_text(slice, COLCOUNT - 8)
output_lines = output_lines[0:10]
print(f"==== output lines ==== {len(output_lines)}")
for line in output_lines:
    print(line)
    # term.print_line(line)

start_line = 0
def paginate():
    end_line = min(start_line+ROWCOUNT, len(output_lines))
    print("line count",len(output_lines), start_line,"to",end_line)

    for i in range(start_line,end_line):
        li = output_lines[i]
        term.print_line(li)

paginate()

# handle input events
while True:
    time.sleep(0.01)
    keypress = tdeck.get_keypress()
    if keypress:
        print("keypress-", keypress,"-")
        if keypress == ' ':
            start_line += (ROWCOUNT-4)
            paginate()
