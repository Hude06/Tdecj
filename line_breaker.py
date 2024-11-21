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

    def wrap_text(self, chunks, max_width):
        lines = []
        line = []
        current_width = 0
        for chunk in chunks:
            name = chunk[0]
            content = chunk[1]
            atts = chunk[2]
            dprint(f"wrapping [{name}] {content} {atts}")
            dprint(f" len = {len(content)}")
            name = remap_name(name)
            if name == 'header':
                dprint("LINE:",line)
                ## finish the current line
                lines.append(line)
                ## add the header
                lines.append([[content,name,atts]])
                ## start new line
                line = []
                current_width = 0
                continue
            if current_width + len(content) > max_width:
                dprint(f"SPLIT: {content}")
                words = content.split()
                before = ""
                for word in words:
                    if current_width + len(before) > max_width:
                        dprint(f"BREAK at word '{word}'",)
                        line.append([before,name,atts])
                        dprint("LINE:",line)
                        yield line
                        lines.append(line)
                        line = []
                        before = ""
                        current_width = 0
                    before += word + " "
                line.append([before,name,atts])
                current_width += len(before)
                continue
            line.append([content,name,atts])
            current_width += len(content)
            # current_width += 1 # account for spaces
        dprint("LINE:",line)
        lines.append(line)
        return lines
