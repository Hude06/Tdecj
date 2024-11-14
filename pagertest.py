import board
import terminalio
import displayio
import time
from helper import TDeck
from paging_terminal import HighlightTerminal
# make some real text
text_nodes = [
    ["Some more plain text that is long and will have to break.","plain"],
    ["Some more plain text that is long and will have to break.","plain"],
    ["Some more plain text that is long and will have to break.","plain"],
    ["Some more plain text that is long and will have to break.","plain"],
    ["A header","header"],
    ["Some more plain text that is long and will have to break.","plain"],
    ["Some more plain text that is long and will have to break.","plain"],
    ["Some more plain text that is long and will have to break.","plain"],
    ["Some more plain text that is long and will have to break.","plain"],
    ["A header","header"],
    ["Some more plain text that is long and will have to break.","plain"],
    ["Some more plain text that is long and will have to break.","plain"],
    ["Some plain text.","plain"],
    ["Some plain text.","plain"],
    ["Some plain text.","plain"],
    ["A header","header"],
    ["A whole bunch of long text that we will need to split.","plain"],
    ["A bold sentence.","bold"],
    ["Some more text.","plain"],
    ["Some more text.","plain"],
    ["A bold word.","bold"],
]

# text_nodes = []
# for i in range(0,100):
#     text_nodes.append([f"line {i} ","plain"])




def wrap_text(text, max_width):
    lines = []
    line = []
    current_width = 0
    for chunk in text:
        if current_width + len(chunk[0]) > max_width:
            # print(f"SPLIT: {chunk[0]}")
            words = chunk[0].split()
            before = ""
            for word in words:
                if current_width + len(before) > max_width:
                    # print(f"BREAK at word '{word}'",)
                    line.append([before,chunk[1]])
                    # print("LINE:",line)
                    lines.append(line)
                    line = []
                    before = ""
                    current_width = 0
                before += word + " "
            line.append([before,chunk[1]])
            current_width += len(before)
            continue
        if chunk[1] == 'header':
            # print("LINE:",line)
            lines.append(line)
            lines.append([chunk])
            line = []
            current_width = 0
            continue
        line.append(chunk)
        current_width += len(chunk[0])
        # current_width += 1 # account for spaces
    # print("LINE:",line)
    lines.append(line)
    return lines


colcount = 40
output_lines = wrap_text(text_nodes,colcount)


tdeck = TDeck()
display = board.DISPLAY
splash = displayio.Group()




display.root_group = splash

# make it be only 5 rows
rowcount = 10
term = HighlightTerminal(rowcount+3,colcount+5)
splash.append(term.group)

start_line = 0
def paginate():
    end_line = min(start_line+rowcount, len(output_lines))
    print("line count",len(output_lines), start_line,"to",end_line)

    for i in range(start_line,end_line):
        li = output_lines[i]
        term.print_line(li)

paginate()
while True:
    keypress = tdeck.get_keypress()
    if keypress:
        print("keypress-", keypress,"-")
        if keypress == ' ':
            start_line += rowcount
            paginate()
        if keypress == 't':
            start_line = 0
            paginate()
        if keypress == 'j':
            start_line += 1
            paginate()
        if keypress == 'k':
            start_line -= 1
            paginate()

    time.sleep(0.05)
