import sys
import unittest
from parser import HtmlParser

DEBUG = False
def dprint(*args, **kwargs):
    if DEBUG:
        print(*args, file=sys.stderr, **kwargs)

def wrap_text(text, max_width):
    lines = []
    line = []
    current_width = 0
    for chunk in text:
        name = chunk[0]
        content = chunk[1]
        dprint(f"wrapping [{name}] {content}")
        if name == 'h1':
            name = 'header'
        if name == 'h2':
            name = 'header'
        if name == 'h3':
            name = 'header'
        if name == 'a':
            name = 'link'
        if name == 'p':
            name = 'plain'
        if current_width + len(content) > max_width:
            dprint(f"SPLIT: {content}")
            words = content.split()
            before = ""
            for word in words:
                if current_width + len(before) > max_width:
                    dprint(f"BREAK at word '{word}'",)
                    line.append([before,name])
                    dprint("LINE:",line)
                    lines.append(line)
                    line = []
                    before = ""
                    current_width = 0
                before += word + " "
            line.append([before,name])
            current_width += len(before)
            continue
        if name == 'header':
            ## finish the current line
            ## add the header
            # print("header line is",line, content, name)
            dprint("LINE:",line)
            lines.append(line)
            lines.append([[content,name]])
            line = []
            current_width = 0
            continue
        line.append([content,name])
        current_width += len(content)
        # current_width += 1 # account for spaces
    dprint("LINE:",line)
    lines.append(line)
    return lines


def print_line(line):
    print("LINE::", line)
    for span in line:
        print(span[0], end="")
    print("")


class LineWrapping(unittest.TestCase):
    def test_short_para(self):
        chunks = [
            ['p',"some cool text"],
        ]
        lines = wrap_text(chunks, 30)
        print("==== lines ====")
        for line in lines:
            print_line(line)
        self.assertEqual(len(lines),1)
        self.assertEqual(lines[0][0][0],"some cool text")

    def test_header_break(self):
        chunks = [
            ['p',"some cool text"],
            ['h1',"a header"],
            ['p', "some cool text"],
        ]
        lines = wrap_text(chunks, 30)
        # lines = list(filter(lambda ln: len(ln[1].strip()) > 0, chunks))
        # print("==== lines ====")
        # for line in lines:
        #     print_line(line)
        self.assertEqual(len(lines),3)
        self.assertEqual(lines[0][0][0],"some cool text")
        self.assertEqual(lines[1][0][0],"a header")
        self.assertEqual(lines[1][0][1],"header")

    def _test_simple_wrapping(self):
        with open("blog.html", "r") as txt:
            html = txt.read()
            parser = HtmlParser()
            chunks = parser.parse(html)
            chunks = list(filter(lambda x: len(x[1].strip())>0,chunks))
            # for chunk in chunks:
            #     print(chunk)
            slice = chunks[1:20]
            # print("==== chunks ====")
            # for chunk in slice:
            #     print(chunk)
            lines = wrap_text(slice, 30)
            print("==== lines ====")
            for line in lines:
                print_line(line)

