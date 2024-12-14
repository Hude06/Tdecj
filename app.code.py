import gc

import board
import time

import displayio
import microcontroller
import wifi

from browser import Browser
from helper import TDeck
from popupmenu import PopupMenu
import adafruit_connection_manager
import adafruit_requests
import vectorio



# Initalize Wifi, Socket Pool, Request Session
# pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
# ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)
# requests = adafruit_requests.Session(pool, ssl_context)


tdeck = TDeck()
display = board.DISPLAY
display.root_group = displayio.Group()

menus = []
def push_menu(menu):
    menus.append(menu)
    display.root_group.append(menu.layout)
def pop_menu(layout):
    pop = menus.pop()
    display.root_group.remove(pop.layout)
def noop(layout):
    print("doing nothing")

def update_menu():
    popup = menus[-1]

    keypress = tdeck.get_keypress()
    if keypress:
        # print("keypress-", keypress, "-")
        if keypress == ' ':
            popup.perform_selected_item()
    click = tdeck.get_click()
    if click and click.pressed:
        popup.perform_selected_item()
    for p, c in tdeck.get_trackball():
        if c > 0:
            if p == "right":
                menus[-1].select_next_item()
            if p == "down":
                popup.select_next_item()
            if p == "left":
                popup.select_prev_item()
            if p == "up":
                popup.select_prev_item()

def show_info(layout):
    info_menu = [
        [f"  used mem: {gc.mem_alloc()/1024}k"],
        [f"  free mem: {gc.mem_free()/1024}k"],
        [f"  cpu temp: {microcontroller.cpu.temperature}C"],
        [f"  cpu freq: {microcontroller.cpu.frequency/(1*1000*1000)}mhz"],
        [f"  Battery Voltage: {tdeck.get_battery_voltage():.2f} V"],
        [ "< Back",pop_menu],
    ]
    push_menu(PopupMenu(info_menu))


def show_status(layout):
    info = [
        [f"radio enabled = {wifi.radio.enabled}",noop],
        [f"connected {wifi.radio.connected}"],
        [f"hostname enabled = {wifi.radio.hostname}",noop],
    ]
    if wifi.radio.connected:
        info.append([f"  ssid {wifi.radio.ap_info.ssid}",noop])
    info.append(["< Back", pop_menu])
    push_menu(PopupMenu(info))

def config_network(layout):
    def scan_networks(layout):
        items = [
            ['< back', pop_menu]
        ]
        for network in wifi.radio.start_scanning_networks():
            print(f"{network.ssid} [Ch:{network.channel}] RSSI: {network.rssi}")
            def connect_network(item):
                print("connecting to",item[2].ssid)
                try:
                    wifi.radio.connect(item[2].ssid, "Jefferson2022")
                    print("connected")
                    pop_menu(None)
                except ConnectionError as ce:
                    print("error connecting",ce)
                    error_menu = [
                        ["Error connecting",noop],
                        ["Okay..",pop_menu]
                    ]
                    push_menu(PopupMenu(error_menu))
            items.append([network.ssid,connect_network,network])
        wifi.radio.stop_scanning_networks()
        push_menu(PopupMenu(items))

    network_menu = [
        ["Network status       ", show_status],
        ["Scan for Wifi        ",scan_networks],
        ["< back               ", pop_menu],
    ]
    push_menu(PopupMenu(network_menu))

browser = None
def start_browser(info):
    print("starting the browser")
    global browser
    wifi_params = {
        "pool": adafruit_connection_manager.get_radio_socketpool(wifi.radio),
        "ssl_context": adafruit_connection_manager.get_radio_ssl_context(wifi.radio),
        "requests": adafruit_requests.Session(
            adafruit_connection_manager.get_radio_socketpool(wifi.radio),
            adafruit_connection_manager.get_radio_ssl_context(wifi.radio),
        ),
        "ssid": "JEFF22",  # You can change this to "JEFF22" if needed
        "password": "Jefferson2022",
    }
    browser = Browser(wifi_params, display, cols=40, page_size=16)
    display.root_group.append(browser.splash)
    browser.load_file("content/links.html")

main_menu = [
    ["Info       ", show_info],
    ["Network    ", config_network],
    ["Browse the web", start_browser]
]

bg_palette = displayio.Palette(1)
bg_palette[0] = 0x125690
bg_rect = vectorio.Rectangle(pixel_shader=bg_palette,
                             width=display.width, height=display.height, x=0, y=0)
display.root_group.append(bg_rect)

push_menu(PopupMenu(main_menu))

def update_browser_nav():
    keypress = tdeck.get_keypress()
    if keypress:
        print("keypressss-", keypress, "-")
        if keypress == ' ':
            browser.page_down()
        if keypress == 'j':
            browser.nav_next_link()
        if keypress == 'k':
            browser.nav_prev_link()
        if keypress == 'g':
            browser.load_selected_link()
    for p, c in tdeck.get_trackball():
        if c > 0:
            if p == "right":
                browser.nav_next_link()
            if p == "down":
                browser.nav_next_link()
            if p == "left":
                browser.nav_prev_link()
            if p == "up":
                browser.nav_prev_link()

while True:
    time.sleep(0.01)
    if browser:
        update_browser_nav()
    update_menu()

