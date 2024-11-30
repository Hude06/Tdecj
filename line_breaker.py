import sys

DEBUG = False
def dprint(*args, **kwargs):
    if DEBUG:
        print(*args, file=sys.stderr, **kwargs)


def remap_name(name):
    if name == 'h1':
        return 'header'
    if name == 'h2':
        return 'header'
    if name == 'h3':
        return 'header'
    if name == 'a':
        return 'link'
    if name == 'p':
        return 'plain'
    if name == 'li':
        return 'plain'
    return name

class LineBreaker:
    def __init__(self):
        pass

    def wrap_text2(self, chunks, max_width):
        # print("wrapping")
        current_width = 0
        for chunk in chunks:
            # print("wrapping chunk",chunk)
            name = remap_name(chunk[0])
            line = [name]
            for span in chunk[2:]:
                # print(f"span type:{span[0]}")
                if span[0] == 'a':
                    text = span[2]
                    # print(f"appending text: '{text}'")
                    line.append(['link',['plain',text[1]],span[1]])
                if span[0] == 'text':
                    text = span[1]
                    # print(f"appending text: '{text}'")
                    while len(text) + current_width > max_width:
                        # print("splitting:",text)
                        n = (max_width - current_width)
                        before = text[:n]
                        # print(f"append before: '{before}'")
                        line.append(['plain',before])
                        yield line
                        line = [name]
                        text = text[n:]
                        # print(f"append after: '{text}'")
                    line.append(['plain', text])
            yield line
            yield ['blank']
        pass



    # def wrap_text(self, chunks, max_width):
    #     print("wrapping",chunks)
    #     lines = []
    #     line = []
    #     current_width = 0
    #     for chunk in chunks:
    #         print('chunk',chunk)
    #         name = chunk[0]
    #         atts = chunk[1]
    #         content = chunk[2]
    #         dprint(f"wrapping {name} {atts} {content}")
    #         dprint(f" len = {len(content)}")
    #         name = remap_name(name)
    #         if name == 'header':
    #             dprint("LINE:",line)
    #             ## finish the current line
    #             lines.append(line)
    #             ## add the header
    #             lines.append([[content,name,atts]])
    #             ## start new line
    #             line = []
    #             current_width = 0
    #             continue
    #
    #         print('content is',content[1])
    #         if current_width + len(content[1]) > max_width:
    #             dprint(f"SPLIT: {content}")
    #             words = content[1].split()
    #             before = ""
    #             for word in words:
    #                 if current_width + len(before) > max_width:
    #                     dprint(f"BREAK at word '{word}'",)
    #                     line.append([before,name,atts])
    #                     dprint("LINE:",line)
    #                     yield line
    #                     lines.append(line)
    #                     line = []
    #                     before = ""
    #                     current_width = 0
    #                 before += word + " "
    #             line.append([before,name,atts])
    #             current_width += len(before)
    #             continue
    #         line.append([content[1],name,atts])
    #         current_width += len(content)
    #         # current_width += 1 # account for spaces
    #     dprint("LINE:",line)
    #     yield line
    #     lines.append(line)
    #     return lines
