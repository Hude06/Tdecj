import unittest
from parser import HtmlParser
from line_breaker import LineBreaker


def print_line(line):
    print("LINE::", line)
    for span in line:
        print(span[0], end="")
    print("")


class LineWrappingTests(unittest.TestCase):
    def test_short_para(self):
        chunks = [
            ['p',"some cool text"],
        ]
        lines = LineBreaker().wrap_text(chunks, 30)
        # print("==== lines ====")
        # for line in lines:
        #     print_line(line)
        self.assertEqual(len(lines),1)
        self.assertEqual(lines[0][0][0],"some cool text")

    def test_header_break(self):
        chunks = [
            ['p',"some cool text"],
            ['h1',"a header"],
            ['p', "some cool text"],
        ]
        lines = LineBreaker().wrap_text(chunks, 30)
        # lines = list(filter(lambda ln: len(ln[1].strip()) > 0, chunks))
        # print("==== lines ====")
        # for line in lines:
        #     print_line(line)
        self.assertEqual(len(lines),3)
        self.assertEqual(lines[0][0][0],"some cool text")
        self.assertEqual(lines[1][0][0],"a header")
        self.assertEqual(lines[1][0][1],"header")

    def test_header_break2(self):
        chunks = [
            ['a', 'Blog'],
            ['a', 'About Josh'],
            ['a', 'Books &amp; Writing'],
            ['a', 'Apps &amp; Projects'],
            ['a', 'Hire Me'],
            ['h2', 'Circuit Python Watch Status'],
        ]
        lines = LineBreaker().wrap_text(chunks, 30)
        # print("==== lines ====")
        # for line in lines:
        #     print_line(line)

    def test_simple_wrapping(self):
        with open("blog.html", "r") as txt:
            html = txt.read()
            parser = HtmlParser()
            chunks = parser.parse(html)
            chunks = list(filter(lambda x: len(x[1].strip())>0,chunks))
            # for chunk in chunks:
            #     print(chunk)
            slice = chunks[1:10]
            print("==== chunks ====")
            for chunk in slice:
                print(chunk)
            lines = LineBreaker().wrap_text(slice, 30)
            print("==== lines ====")
            for line in lines:
                print_line(line)

