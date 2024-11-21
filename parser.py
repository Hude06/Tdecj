import re
import sys

DEBUG = False
def dprint(*args, **kwargs):
    if DEBUG:
        print(*args, file=sys.stderr, **kwargs)

paraTags = ["h1","h2","h3","h4","p","li","td"]
solo_tags = ['img']
ignore_tags = ['meta','link', "!DOCTYPE",'script','title','head','html','body']

MAX_TEXT = 2500_0
class HtmlParser:
    def __init__(self):
        self.stack = []
        self.run = ""
        self.runs = []
        self.n = 0

    def parse(self, text):
        # print("processing text",text[0:MAX_TEXT])
        self.n = 0
        self.runs = []
        self.run = ""

        while self.n < len(text) and self.n < MAX_TEXT:
            ch = text[self.n]
            dprint(self.n,"char -",ch,"-")

            if text[self.n:self.n+len("</")] == "</":
                self.end_tag(text,self.n)
                dprint("elem is", self.runs)
                if len(self.runs) < 1:
                    dprint("not enough space")
                else:
                    elem = self.runs[len(self.runs)-1]
                    dprint("the end tag is", elem)
                    yield elem
                self.run = ""
                continue
            if text[self.n] == "<":
                self.slurp_tag(text,self.n)
                continue

            if ch == '\n':
                ch = ""
            self.run += ch
            self.n += 1
            dprint('self run:-', self.run,"-")
        self.save_run()
        return self.runs

    def slurp_tag(self, text, n):
        self.save_run()
        end_index = text.find(">",n+1)
        space_index = text.find(' ',n+1,end_index)
        name = text[n+1:end_index]
        # print(f"slurping tag '{name}'")
        if space_index >= 0:
            name = text[n+1:space_index]
        name = name.strip()
        if  not (name in ignore_tags):
            attrs_str = text[n+1 + len(name):end_index]
            atts = self.parse_attributes(attrs_str)
            # print(f"start elem '{name}'",atts)
            self.stack.append([name,atts])
        if name in solo_tags:
            res = self.stack.pop()
            # print(f"popping solo tag '{res[0]}'", text[n+1:end_index])
            self.runs.append([res[0],''])
        self.n = end_index+1

    def end_tag(self,text,n):
        end_index = text.find(">",n+1)
        name = text[n+2:end_index]
        dprint("end tag name",name)
        if name in ignore_tags:
            dprint("should ignore",name)
            self.n = end_index+1
            return
        res = self.stack.pop()
        dprint("pop",res[0])
        if name != res[0]:
            dprint("pop mismatch", text[n+2:end_index],'vs',res)
        txt = self.run.strip()
        if len(txt) > 0:
            self.append_content(name,txt, res[1])
        self.n = end_index+1

    def save_run(self):
        txt = self.run.strip()
        if len(txt) > 0:
            dprint(f"saving run: '{txt}'")
            name = 'plain'
            if len(self.stack) > 0 and self.stack[-1]:
                name = self.stack[-1][0]
            self.append_content(name,txt)

    def append_content(self, name, content, attrs=None):
        # print("appending",content)
        content = re.sub(r"&amp;", '&', content)
        content = re.sub(r"&#x27;", "'", content)
        self.runs.append([name,content,attrs])
        self.run = ""

    def parse_attributes(self, attrs_str):
        # print(f"pushing tag '{name}':'{attrs_str}'")
        attribs = attrs_str.split(" ")
        atts = {}
        # print("pairs",attribs)
        for attr_str in attribs:
            # print(f"pair {attr_str}")
            if len(attr_str.strip()) > 0:
                pair = attr_str.split("=")
                # print("split", pair)
                if len(pair) == 2:
                    value = pair[1].strip()
                    if value.startswith('"'):
                        # print("get rid of quotes", value)
                        value = value[1:-1]
                    atts[pair[0]] = value
        return atts

def process_html(html):
    parser = HtmlParser()
    chunks = parser.parse(html)
    return chunks


