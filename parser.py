paraTags = ["h1","h2","h3","h4","p","li","td"]
ignore_tags = ['meta','link', "!DOCTYPE",'script','title','head','html','body']

MAX_TEXT = 2500_0
class HtmlParser:
    def __init__(self):
        self.stack = []
        self.run = ""
        self.runs = []
        self.n = 0

    def parse(self, text):
        print("processing text",text[0:MAX_TEXT])
        self.n = 0
        self.runs = []
        self.run = ""

        while self.n < len(text) and self.n < MAX_TEXT:
            if text[self.n:self.n+len("</")] == "</":
                self.end_tag(text,self.n)
                self.run = ""
                continue
            if text[self.n] == "<":
                self.slurp_tag(text,self.n)
                continue

            ch = text[self.n]
            self.run += ch
            self.n += 1
            # print(self.run)
        self.save_run()
        return self.runs

    def slurp_tag(self, text, n):
        end_index = text.find(">",n+1)
        space_index = text.find(' ',n+1,end_index)
        name = text[n+1:end_index]
        # print("slurping tag",name)
        # print(space_index, end_index)
        # , '-'+text[n+1:space_index]+'-','vs','-'+text[n+1:end_index]+'-')
        if space_index >= 0:
        # if space_index < end_index:
            name = text[n+1:space_index]
        if  not (name in ignore_tags):
            # print("push",name, text[n+1:end_index])
            self.stack.append([name,text[n+1:end_index]])
        self.save_run()
        # if len(self.run) > 0:
            # print("lost run:['"+name+"', '"+self.run+"']")
            # self.runs.append(['plain',self.run])
            # self.run = ""
        self.n = end_index+1

    def end_tag(self,text,n):
        end_index = text.find(">",n+1)
        name = text[n+2:end_index]
        if name in ignore_tags:
            # print("should ignore",name)
            self.n = end_index+1
            return
        res = self.stack.pop()
        # print("pop",res[0])
        if name != res[0]:
            print("pop mismatch", text[n+2:end_index],'vs',res)
        if len(self.run) > 0:
            # print("run:['"+name+"', '"+self.run+"']")
            self.runs.append([name,self.run])
            self.run = ""
        self.n = end_index+1

    def save_run(self):
        if len(self.run) > 0:
            # print("run:", self.run)
            self.runs.append(['plain',self.run])
            self.run = ""


def process_html(html):
    parser = HtmlParser()
    chunks = parser.parse(html)
    return chunks


