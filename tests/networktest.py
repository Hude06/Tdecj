import time

from browser import Browser
from parser import HtmlParser

import adafruit_connection_manager
import adafruit_requests
import adafruit_ntp
import board
import displayio
import terminalio
import wifi

from helper import TDeck

# init highlighter
wifi_params = {
    "pool": adafruit_connection_manager.get_radio_socketpool(wifi.radio),
    "ssl_context": adafruit_connection_manager.get_radio_ssl_context(wifi.radio),
    "requests": adafruit_requests.Session(
        adafruit_connection_manager.get_radio_socketpool(wifi.radio),
        adafruit_connection_manager.get_radio_ssl_context(wifi.radio),
    ),
    #"ssid": "JEFF22",  # You can change this to "JEFF22" if needed
    "ssid":"Vero-Public",
    # "password": "Jefferson2022",
    "password":"",
}


print("scanning for networks")
networks = []
for network in wifi.radio.start_scanning_networks():
    networks.append(network)
wifi.radio.stop_scanning_networks()
networks = sorted(networks, key=lambda net: net.rssi, reverse=True)
for network in networks:
    print("ssid:",network.ssid, "rssi:",network.rssi)



# Now connect using the correct wifi parameters
print("connecting to wifi")
wifi.radio.connect(wifi_params["ssid"], wifi_params["password"])
print("connected to wifi")


def _format_datetime(datetime):
    return "{:02}/{:02}/{} {:02}:{:02}:{:02}".format(
        datetime.tm_mon,
        datetime.tm_mday,
        datetime.tm_year,
        datetime.tm_hour,
        datetime.tm_min,
        datetime.tm_sec,
    )


ntp = adafruit_ntp.NTP(wifi_params['pool'], tz_offset=0, cache_seconds=3600)
while True:
    print("current date time", ntp.datetime)
    # formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", ntp.datetime)
    # print("formatted time", formatted_time)
    print("formatted time", _format_datetime(ntp.datetime))
    print("my IP addr:", wifi.radio.ipv4_address)
    print("current wifi:", wifi.radio.ap_info.ssid)
    print("signal strength", wifi.radio.ap_info.rssi)
    time.sleep(5)

