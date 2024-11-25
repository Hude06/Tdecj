import re
import sys

DEBUG = False
def dprint(*args, **kwargs):
    if DEBUG:
        print(*args, file=sys.stderr, **kwargs)

paraTags = ["h1","h2","h3","h4","p","li","td"]
solo_tags = ['img']

ignore_tags = ['meta','link', "!DOCTYPE",'script','title','head','html','body']

block_elements = ['p','h1','h2','h3','h4','h5','div','li']

MAX_TEXT = 2500_0
class HtmlParser:
    def __init__(self):
        self.elems = []
        self.span = ""
        self.n = 0

    def parse(self, text):
        # print("processing text",text[0:MAX_TEXT])
        self.n = 0
        self.elems = []
        self.span = ""

        while self.n < len(text) and self.n < MAX_TEXT:
            ch = text[self.n]
            # dprint(self.n,f"char '{ch}'")

            # end element
            if text[self.n:self.n+len("</")] == "</":
                dprint("ending element")
                end_index = text.find(">", self.n + 1)
                name = text[self.n + 2:end_index]
                dprint("end tag name", name)
                elem = self.elems.pop()
                # print("ending elem",elem)

                elem.append(self.make_span(self.span))
                self.span = ""

                # print("ending elem",elem)
                if elem[0] in block_elements:
                    # print("yielding block",elem)
                    yield elem
                else:
                    # print("appending to parent")
                    if elem[0] not in ignore_tags:
                        if len(self.elems) > 0:
                            self.elems[-1].append(elem)
                        else:
                            print("no parent to append to!",elem)
                    else:
                        dprint("ignoring element",elem[0])
                self.n = end_index + 1
                continue

            # start element
            if text[self.n] == "<":
                parent = ['block']
                if len(self.elems) > 0:
                    parent = self.elems[-1]
                # print("adding spans to parent",self.span)
                self.append_span(parent)
                if parent[0] == 'block' and len(parent) > 1:
                    yield parent
                self.span = ""
                elem = self.start_elem(text)
                self.elems.append(elem)
                continue

            # skip newlines
            # if ch == '\n':
            #     ch = ""
            self.span += ch
            self.n += 1
            # dprint('run:-', self.run,"-")
        # print("done")

        # any remaining text
        # if self.span != "":
        block = ['block']
        # print("span is", self.span, len(self.span))
        self.append_span(block)
        # block = ['block', self.make_span(self.span)]
        # print("final block is",block)
        if len(block) > 1:
            yield block

    def start_elem(self, text):
        end_index = text.find(">", self.n + 1)
        # space_index = text.find(' ', self.n + 1, end_index)
        name = text[self.n + 1:end_index]
        # print("name",name)
        attrs_str = text[self.n + 1 + len(name):end_index]
        atts = self.parse_attributes(attrs_str)
        # print(f"start elem '{name}'",atts)
        self.n = end_index+1
        self.span = ""
        return [name,atts]

    # def slurp_tag(self, text, n):
    #     self.save_run()
    #     end_index = text.find(">",n+1)
    #     space_index = text.find(' ',n+1,end_index)
    #     name = text[n+1:end_index]
    #     print(f"slurping tag '{name}'")
    #     if space_index >= 0:
    #         name = text[n+1:space_index]
    #     name = name.strip()
    #     if  not (name in ignore_tags):
    #         attrs_str = text[n+1 + len(name):end_index]
    #         atts = self.parse_attributes(attrs_str)
    #         # print(f"start elem '{name}'",atts)
    #         self.elems.append([name, atts])
    #     if name in solo_tags:
    #         res = self.elems.pop()
    #         # print(f"popping solo tag '{res[0]}'", text[n+1:end_index])
    #         self.spans.append([res[0], ''])
    #     self.n = end_index+1

    # def end_tag(self,text,n):
    #     end_index = text.find(">",n+1)
    #     name = text[n+2:end_index]
    #     dprint("end tag name",name)
    #     # if name in ignore_tags:
    #     #     dprint("should ignore",name)
    #     #     self.n = end_index+1
    #     #     return
    #     res = self.elems.pop()
    #     dprint("pop",res[0])
    #     if name != res[0]:
    #         dprint("pop mismatch", text[n+2:end_index],'vs',res)
    #     txt = self.span.strip()
    #     if len(txt) > 0:
    #         self.append_content(name,txt, res[1])
    #     self.n = end_index+1
    #     return res

    # def save_run(self):
    #     txt = self.span.strip()
    #     if len(txt) > 0:
    #         dprint(f"saving run: '{txt}'")
    #         name = 'plain'
    #         if len(self.elems) > 0 and self.elems[-1]:
    #             name = self.elems[-1][0]
    #         self.append_content(name,txt)

    def make_span(self, content):
        content = content.strip()
        content = re.sub(r"&amp;", '&', content)
        content = re.sub(r"&#x27;", "'", content)
        return ['text',content]

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

    def append_span(self, block):
        if self.span.strip() == "":
            return
        block.append(self.make_span(self.span))


def process_html(html):
    parser = HtmlParser()
    chunks = parser.parse(html)
    return chunks


