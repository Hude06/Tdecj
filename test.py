import parser
import requests

# x = requests.get('https://joshondesign.com/c/writings')
x = requests.get('https://joshondesign.com/2023/07/25/circuitpython-watch')
chunks = parser.process_html(x.text)
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
        continue
    if chunk[0] == 'a':
        print("LINK ", chunk[1])
        continue
    print(chunk)

# f = open('test.html')
# parser.process_html(f.read())
