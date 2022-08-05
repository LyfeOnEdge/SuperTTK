INTRO = """
Auto-Generated with SuperTTK
"""
STYLE = """
<style>
html { filter: invert(1); }
body {
  background-color: linen;
}
div {
  background-color: #cccccc;
  padding: 10px;
  border-radius: 80px;
}
input.larger {
    width: 30px;
    height: 30px;
    padding: 0px;
}
.general-theme {
  background: #222220;
  color: #ddd;
}
</style>
"""

class HTML_Generator:
    def __init__(self, indent="\t"):
        self.current_depth = 1
        self.indent_type = indent
        self.intro = f"<!--{INTRO}-->\n"
        self.doctype = "<!doctype html>\n"
        self.html_start = '<html lang="en">\n'
        self.head = self.get_indent() + "<head>\n"
        self.current_depth += 1
        self.head += self.get_indent() + '<meta charset="utf-8">\n'
        self.current_depth -= 1
        self.head += STYLE
        self.head += self.get_indent() + "</head>\n"
        self.body_start = self.get_indent() + "<body>\n"
        self.body = ""
        self.body_end = self.get_indent() + "</body>\n"
        self.html_end = "</html>\n"
        self.current_depth += 1

    # FUNCTIONAL CODE
    def get_indent(self, offset=0):
        return (self.current_depth + offset) * self.indent_type

    def assemble(self):
        out = ""
        for i in [
            self.intro,
            self.doctype,
            self.html_start,
            self.head,
            self.body_start,
            self.body,
            self.body_end,
            self.html_end,
        ]:
            out += i
        return out

    def save(self, path):
        with open(path, "w+") as f:
            f.write(self.assemble())

    # /FUNCTIONAL CODE

    def add_body_line(self, text=""):
        if text:
            self.body += self.get_indent() + text + "\n"

    def add_comment(self, text):
        self.add_body_line("<!--")
        self.add_body_line(text)
        self.add_body_line("-->")

    # DIV
    def start_div(self, text=""):
        self.body += self.get_indent() + "<div>\n"
        self.current_depth += 1
        self.add_body_line(text)

    def add_div(self, text=""):
        self.start_div(text)
        self.end_div()

    def end_div(self):
        self.current_depth -= 1
        self.body += self.get_indent() + "</div>\n"

    # /DIV

    # BOLD
    def start_bold(self, text=""):
        self.body += self.get_indent() + "<b>\n"
        self.current_depth += 1
        self.add_body_line(text)

    def add_bold(self, text=""):
        self.start_bold(text)
        self.end_bold()

    def end_bold(self):
        self.current_depth -= 1
        self.body += self.get_indent() + "</b>\n"

    # /BOLD

    # PARAGRAPH
    def start_paragraph(self, text=""):
        self.body += self.get_indent() + "<p>\n"
        self.current_depth += 1
        self.add_body_line(text)

    def add_paragraph(self, text=""):
        self.start_paragraph(text)
        self.end_paragraph()

    def end_paragraph(self):
        self.current_depth -= 1
        self.body += self.get_indent() + "</p>\n"

    # /PARAGRAPH

    # CENTER
    def start_center(self, text=""):
        self.body += self.get_indent() + "<center>\n"
        self.current_depth += 1
        self.add_body_line(text)

    def add_center(self, text=""):
        self.start_center(text)
        self.end_center()

    def end_center(self):
        self.current_depth -= 1
        self.body += self.get_indent() + "</center>\n"

    # /CENTER

    # ETC
    def add_divider(self):
        self.body += self.get_indent() + "<hr>\n"

    # LIST
    def start_list(self, items=[], ordered=False):
        self.body += self.get_indent() + "<ol>" if ordered else "<ul>" + "\n"
        self.current_depth += 1
        for i in items:
            self.add_list_item(i)
        
    def add_list(self, items=[], ordered=False):
        self.start_list(items=items, ordered=ordered)
        self.end_list(ordered=ordered)

    def end_list(self, ordered=False):
        self.current_depth -= 1
        self.body += self.get_indent() + "</ol>" if ordered else "</ul>" + "\n"

    def add_list_item(self, item:str):
        self.body += self.get_indent() + f"<li>{item}</li>\n"

if __name__ == "__main__":
    import webbrowser

    generator = HTML_Generator()
    r = 50
    for i in range(r):
        generator.start_div()
        generator.add_center('<input type="checkbox" class="larger">')
        generator.add_center(f'<h>{str(i)}</h>')
        if i < r-1:
            generator.end_div()
            generator.add_divider()
    print(generator.assemble())
    generator.save("out.html")
    webbrowser.open("out.html")
