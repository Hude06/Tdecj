import unittest
from parser import HtmlParser
from line_breaker import LineBreaker


def print_line(line):
    print("LINE::", line)
    for span in line[1:]:
        print(span[1], end="")
    print("")


def render_line(line):
    for span in line[1:]:
        print(span[1], end="")
    print("")


class LineWrappingTests(unittest.TestCase):
    def test_short_para(self):
        chunks = [
            ['p',{},['text',"some plain text"]],
        ]

        lines = list(LineBreaker().wrap_text2(chunks, 30))

        # ['p', {}, ['text', 'some plain text']],
        # # becomes
        # [
        #     ['line', ['plain', 'some plain text']]
        # ],

        # print("==== lines ====")
        # for line in lines:
        #     print_line(line)
        self.assertEqual(2,len(lines))
        self.assertEqual("some plain text",lines[0][1][1])
        self.assertEqual("blank",lines[1][0])

    def test_long_para(self):
        chunks = [
            ['p',{},['text',"Some very cool text that is super very long and then more cool text and then some even more cool text"]],
        ]
        lines = list(LineBreaker().wrap_text2(chunks, 30))
        # print("==== lines ====")
        # for line in lines:
        #     print_line(line)
        self.assertEqual(5,len(lines))

    def test_header_para(self):
        chunks = [
            ['h1',{}, ['text', 'HTML Test']],
            ['p', {},
             ['text', 'One of my original']
             ],
        ]
        lines = list(LineBreaker().wrap_text2(chunks, 30))
        # print("==== lines ====")
        # for line in lines:
        #     print_line(line)
        self.assertEqual(4,len(lines))
        header = lines[0]
        self.assertEqual("header", header[0])
        self.assertEqual("HTML Test", header[1][1])

    def test_link_wrapping(self):
        chunks = [
            ['p',{},['a',{'href':'links.html'},['text','this page']]]
        ]
        lines = list(LineBreaker().wrap_text2(chunks, 30))
        # print("==== lines ====")
        # for line in lines:
            # print(line)
            # print_line(line)
        self.assertEqual(2,len(lines))
        self.assertEqual(lines[0],['plain',['link',['plain','this page'],{'href':'links.html'}]])

    def test_blog_wrapping(self):
        with open("blog.html", "r") as txt:
            html = txt.read()
            chunks = list(HtmlParser().parse(html))
            # chunks = list(filter(lambda x: len(x[1].strip())>0,chunks))
            all_lines = []
            for chunk in chunks:
                # print("==== chunk ====")
                # print(chunk)
                lines = LineBreaker().wrap_text2([chunk], 40)
                # print("converted to lines")
                for line in lines:
                    # print_line(line)
                    # render_line(line)
                    all_lines.append(line)
            # print("==== lines ====")
            # for line in all_lines:
            #     render_line(line)

    # def test_links(self):
    #     with open("links.html", "r") as txt:
    #         html = txt.read()
    #         parser = HtmlParser()
    #         chunks = parser.parse(html)
    #         chunks = list(filter(lambda x: len(x[1].strip())>0,chunks))
    #         # for chunk in chunks:
    #         #     print(chunk)
    #         slice = chunks[1:10]
    #         print("==== chunks ====")
    #         for chunk in slice:
    #             print(chunk)
    #         lines = LineBreaker().wrap_text(slice, 30)
    #         print("==== lines ====")
    #         for line in lines:
    #             print_line(line)

