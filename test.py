import parser
import requests

x = requests.get('https://joshondesign.com/c/writings')
parser.process_html(x.text)
