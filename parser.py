#import requests

# f = open("demofile.html")
# html = f.read()

#x = requests.get('https://joshondesign.com/c/projects')
# x = requests.get('https://news.ycombinator.com/')
#html = x.text

#print("text is",html)
index = 0
inside_para = False
paras = []
line = ""

def starts_with(html,index,str):
    # print("html is",html)
    # print("index",index)
    # print("str",str)
    sub = html[index: index + len(str)]
    # print("sub is",sub)
    return sub == str

paraTags = ["h1","h2","h3","h4","p","li","td"]

def check_tags(html, char):
    global index
    global inside_para
    global line
    for tag in paraTags:
        open_tag = "<"+tag+">"
        close_tag = "</"+tag+">"
        if html[index: index + len(open_tag)] == open_tag:
            # print(open_tag)
            index += len(open_tag)
            inside_para = True
            return
        if html[index: index + len(close_tag)] == close_tag:
            # print(close_tag)
            index += len(close_tag)
            paras.append(line)
            line = ""
            inside_para = False
            return
    # print("char",char,"inside",inside_para)
    if inside_para:
        line = line + char
    index += 1

def split_chunks(text):
    # print("processing text",text)
    n = 0
    stack = []
    runs = []
    run = ""
    while n < len(text):
        if text[n:n+len("</")] == "</":
            res = stack.pop()
            # print("pop",res)
            # print("adding run popped:", run)
            runs.append(['link',res,run])
            run = ""
        if text[n:n+len("<")] == "<":
            # print("push tag")
            end_index = text.find(">",n)
            # print("tag contents",text[n:end_index+1])
            stack.append(text[n:end_index])
            # print("adding run:", run)
            runs.append(['plain',run])
            n = end_index+1
            run = ""
            continue
        run += text[n]
        n += 1
    runs.append(['plain',run])
    # print("runs",runs)
    return runs

def process_html(html):
    # print("processing",html)
    global index
    index = 0
    while index < len(html):
        check_tags(html, html[index])

    chunks = []
    for para in paras:
        chunks.append(['para',split_chunks(para)])

    for chunk in chunks:
        # print("type",chunk[0])
        for run in chunk[1]:
            if run[0] == 'plain':
                if len(run[1]) > 0:
                    print(run[1], end='')
            if run[0] == 'link' and len(run[2]) > 0:
                print("*"+run[2]+"*", end='')
        print("")



