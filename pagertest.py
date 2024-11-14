
# make some real text
text = [
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

# wrap into 40 char wide lines
lines = []
max_width = 30

print("text: ",text)
line = []
current_width = 0
for chunk in text:
    if current_width + len(chunk[0]) > max_width:
        print(f"SPLIT: {chunk[0]}")
        words = chunk[0].split()
        before = ""
        for word in words:
            if current_width + len(before) > max_width:
                print(f"BREAK at word '{word}'",)
                line.append([before,chunk[1]])
                print("LINE:",line)
                lines.append(line)
                line = []
                before = ""
                current_width = 0
            before += word + " "
        line.append([before,chunk[1]])
        current_width += len(before)
        continue
    if chunk[1] == 'header':
        print("LINE:",line)
        lines.append(line)
        lines.append([chunk])
        line = []
        current_width = 0
        continue
    line.append(chunk)
    current_width += len(chunk[0])
    # current_width += 1 # account for spaces
print("LINE:",line)
lines.append(line)

def print_line(line):
    out = ""
    for sect in line:
        if sect[1] == "header":
            out += "\n# " + sect[0] + "\n"
        if sect[1] == "link":
            out += "*" + sect[0] + "*" + " "
        if sect[1] == "bold":
            out += "*" + sect[0] + "*" + " "
        if sect[1] == 'plain':
            out += sect[0] + " "
    # print("line:",line)
    print(out)

def print_ruler():
    ten = "        "
    o = ""
    for n in range(0,int(max_width/10)+1):
        o += str(n) + "0" + ten
    print(o)

    ten2 = "|123456789"
    oo = ""
    for n in range(0,int(max_width/10)+1):
        oo += ten2
    print(oo)

print_ruler()
print("")
for line in lines:
    print_line(line)
print("")







