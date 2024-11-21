import unittest

from line_breaker import LineBreaker
from parser import HtmlParser
# import requests

class BasicParsing(unittest.TestCase):
    def simple_element(self,text,name,content):
        parser = HtmlParser()
        chunks = parser.parse(text)
        print(chunks)
        self.assertEqual(len(chunks),1)
        self.assertEqual(chunks[0][0], name)
        self.assertEqual(chunks[0][1], content)

    def test_loop(self):
        print("before")
        n = 0
        while n < 5:
            print("n is",n)
            n = n + 1
            if n > 2:
                continue
            print("after")


    def test_elements(self):
        text = ("<body>"
              "<p>some text</p>"
              "<p>some more text</p>"
              "</body>"
              )

        parser = HtmlParser()
        for chunk in parser.parse(text):
            print("the chunk is",chunk)

    def test_wrapping(self):
        text = ("<body>"
              "<p>some text</p>"
              "<p>some very long text that needs to be wrapped and more text to wrap</p>"
              "</body>"
              )
        parser = HtmlParser()
        lb = LineBreaker()
        for chunk in parser.parse(text):
            # print("the chunk is",chunk)
            for line in lb.wrap_text([chunk],30):
                print("line is",line[0])
            # print("result is",res)
            # for block in res:
            #     print("    block is",block)
            #     for span in block:
            #         print("        span is", span)

