import unittest
from parser import HtmlParser
import requests


class BasicParsing(unittest.TestCase):
    def simple_element(self,text,name,content):
        parser = HtmlParser()
        chunks = list(parser.parse(text))
        print(chunks,len(chunks))
        self.assertEqual(len(chunks),1)
        self.assertEqual(chunks[0][0], name)
        self.assertEqual(chunks[0][1], content)

    def test_elements(self):
        self.simple_element("<h1>some html</h1>","h1","some html")
        self.simple_element("<h1 extra>some html</h1>","h1","some html")
        self.simple_element("<a>some html</a>","a","some html")
        self.simple_element("<b>some html</b>","b","some html")
        self.simple_element("<i>some html</i>","i","some html")
        self.simple_element('<a href="foo">some html</a>',"a","some html")
        self.simple_element('<a\n href="foo">some html</a>',"a","some html")
        # self.simple_element('<img\n src="foo" alt="z" />',"img",'')
        # self.simple_element("<li>some html</li>","li","some html")

    def test_whitespace_removal(self):
        self.simple_element("  <h1>   some html  </h1>  ","h1","some html")
        self.simple_element("  <a>   some html  </a>  ","a","some html")
    def test_entity_replacement(self):
        self.simple_element('<a href="foo">foo & bar</a>  ', "a", "foo & bar")
        self.simple_element('<a href="foo">foo &amp; bar</a>  ', "a", "foo & bar")
        self.simple_element('<a href="foo">foo &#x27; bar</a>  ', "a", "foo ' bar")


    def test_link(self):
        parser = HtmlParser()
        chunks = parser.parse('<a href="https://google.com/">link to google</a>')
        print(chunks)
        self.assertEqual(chunks[0][0], "a")
        self.assertEqual(chunks[0][1], "link to google")
        self.assertEqual(chunks[0][2]['href'], "https://google.com/")

    def test_para_with_styles(self):
        parser = HtmlParser()
        chunks = list(parser.parse('<p>before\n<b>middle</b>\nafter</p>'))
        # print("==== chunks ====")
        # print(chunks)
        self.assertEqual(chunks[0][0], "p")
        self.assertEqual(chunks[1][0], "b")
        self.assertEqual(chunks[2][0], "p")


    def test_live(self):
        with open("test.html", "r") as txt:
            html = txt.read()
            # print("opened the file", html)
            parser = HtmlParser()
            chunks = parser.parse(html)
            chunks = list(filter(lambda x: len(x[1].strip())>0,chunks))
            for chunk in chunks:
                print(chunk)
            self.assertEqual(len(chunks),3)

    def test_blog_local(self):
        with open("blog.html", "r") as txt:
            html = txt.read()
            # print("opened the file", html)
            parser = HtmlParser()
            chunks = parser.parse(html)
            # chunks = list(filter(lambda x: len(x[1].strip())>0,chunks))
            self.assertEqual(len(chunks),35)

    def test_blog_remote(self):
        text_url = "https://joshondesign.com/2023/07/25/circuitpython-watch"
        with requests.get(text_url) as response:
            print("got the page",text_url)
            print(f"{len(response.text)} bytes")
            html = response.text
            parser = HtmlParser()
            chunks = parser.parse(html)
            slice = chunks[1:50]
            # chunks = list(filter(lambda x: len(x[1].strip())>0,chunks))
            print("==== chunks ====")
            for chunk in slice:
                print(chunk)
            self.assertEqual(len(chunks),35)


if __name__ == '__main__':
    unittest.main()
