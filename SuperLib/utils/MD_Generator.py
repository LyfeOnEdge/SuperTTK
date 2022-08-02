class MD_Generator:
    def __init__(
        self,
        title=None,
        footnote_title="Notes:",
        footnote_heading_level=2,
        numbered_toc=False,
    ):
        self.title = title
        self.slogan = None
        self.footnote_title = footnote_title
        self.footnote_heading_level = footnote_heading_level
        self._footnotes = []
        self._footnote_index = 1
        self.body = ""
        self.quote_depth = 0


        self.toc_uid_format = "mark{}"
        self.toc_uid = 0
        self.toc_contents = ""
        self.toc_depth = 0
        self.toc_indicies = {}
        
        self.numbered_toc = numbered_toc

        self.home_mark_name = self.toc_uid_format.format(self._get_toc_uid())
        self.home_mark = f'<a name="{self.home_mark_name}"></a>'
        self.toc_marks = {0:self.home_mark_name,1:self.home_mark_name}
        self.last_mark = self.home_mark_name
    
    def set_slogan(self, slogan):
        self.slogan = slogan

    def _get_toc_uid(self):
        self.toc_uid += 1
        return self.toc_uid - 1

    def increase_toc_depth(self):
        self.toc_depth += 1
        self.toc_indicies[self.toc_depth] = 0
        self.toc_marks[self.toc_depth] = self.last_mark

    def decrease_toc_depth(self):
        if self.toc_depth == 0:
            raise ValueError("toc depth already at 0.")
        self.toc_depth -= 1

    def add_toc(self, title, end="\n\n"):
        mark_name = self.toc_uid_format.format(self._get_toc_uid())
        self.last_mark = mark_name
        self.body += f'<a name="{mark_name}"></a>[^](#{self.toc_marks[self.toc_depth]}){end}'
        if self.toc_depth in self.toc_indicies:
            index = self.toc_indicies[self.toc_depth]
        else:
            self.toc_indicies[self.toc_depth] = index = 0
        val = index if self.numbered_toc else "-"
        self.toc_contents += (
            "\t" * self.toc_depth + f"{val} [{title}](#{mark_name})\n"
        )
        self.toc_indicies[self.toc_depth] = index + 1

    def assemble(self):
        #Add home marker
        out = ""
        if self.title:
            out = f"# {self.title}"
        out += f"{self.home_mark}\n\n"
        if self.slogan:
            out += f"***{self.slogan}***\n\n"
        out += "---\n\n"
        if self.toc_contents:
            out += self.toc_contents + "\n\n"
        out += "---\n\n"
        out += self.body
        if self._footnotes:
            for n in range(self._footnote_index):
                out += f"[^{n+1}]: {self._footnotes[n]}."
        return out

    def insert_footnote(self, text):
        self.body += f"[^{self._footnote_index}]"
        self._footnotes.append(text)
        self._footnote_index += 1

    def save(self, path):
        with open(path, "w+") as f:
            f.write(self.assemble())

    def add_bold(self, text, end="\n\n"):
        self.body += f"**{text}**{end}"

    def add_italic(self, text, end="\n"):
        self.body += f"*{text}*{end}"

    def add_bold_italic(self, text, end="\n"):
        self.body += f"*{text}*{end}"

    def add_break(self):
        self.body += "<br>"

    def _add_heading(self, text, level=1, end="\n\n", add_toc=False):
        if not level or level < 0 or level > 6:
            raise ValueError(f"Invalid heading level - {level}")
        self.body += self.get_prefix() + "#" * level + f" {text}"
        if add_toc:
            self.add_toc(text)
        self.body += end

    def add_heading_1(self, text, **kwargs):
        self._add_heading(text, 1, **kwargs)

    def add_heading_2(self, text, **kwargs):
        self._add_heading(text, 2, **kwargs)

    def add_heading_3(self, text, **kwargs):
        self._add_heading(text, 3, **kwargs)

    def add_heading_4(self, text, **kwargs):
        self._add_heading(text, 4, **kwargs)

    def add_heading_5(self, text, **kwargs):
        self._add_heading(text, 5, **kwargs)

    def add_heading_6(self, text, **kwargs):
        self._add_heading(text, 6, **kwargs)

    def add_paragraph(self, text, end="\n\n"):
        self.body += f"{self.get_prefix()}{text}{end}"

    def get_prefix(self):
        return "> " * self.quote_depth

    def add_blockquote(self, text, end="\n\n"):
        self.quote_depth += 1
        self.add_paragraph(f"{text}", end)
        self.quote_depth -= 1

    def add_multi_blockquote(self, texts):
        i = 0
        end = len(texts) - 1
        for t in texts:
            self.add_blockquote(t, end="\n")
            if not i == end:
                self.body += ">\n"
            i += 1

    def add_to_unordered_list(self, text, indent=0):
        self.body += "\t" * indent + f"- {text}"

    def add_unordered_list(self, texts, indent=0):
        for t in texts:
            self.add_to_unordered_list(t, indent)

    def add_to_ordered_list(self, index, text, indent=0):
        self.body += "\t" * indent + f"{index}. {text}"

    def add_ordered_list(self, texts, indent=0):
        i = 1
        for t in texts:
            self.add_to_ordered_list(i, t, indent)
            i += 1

    def add_code_block(self, text, lang="", end="\n"):
        p = self.get_prefix()
        self.body += f"{p}```{lang}\n{p}{text}\n{p}```{end}"

    def add_horizontal_rule(self):
        self.body += f"{self.get_prefix()}---\n\n"

    def add_link(self, link, text=None, tooltip=None):
        if not text:
            text = link
        if tooltip:
            self.body += f'[{text}]({link} "{tooltip}")'
        else:
            self.body += f"[{text}]({link})"


# if __name__ == "__main__":
# from .. import WIDGET_LIST

# widget_names = sorted(w.name for w in WIDGET_LIST)
# generator = MD_Generator(
#     title="SuperTTK", footnote_title="References", footnote_heading_level=2
# )
# generator.add_heading_2("About")
# generator.add_paragraph(
#     "SuperTTK exists because I got tired of re-writing the same bits of TK code over and over"
# )
# generator.add_paragraph(
#     "Not all widgets follow the same arg/kwarg pattern, not all of the code here is the best / most straightforward, but it's a good library to pull from for fast-tracking etc."
# )
# generator.add_paragraph(
#     "Code pulls to improve consistency and functionality are greatly appreciated!"
# )

# print(generator.assemble())
