class TXT_Generator:
    def __init__(self):
        self.body = ""

    def assemble(self):
        return self.body

    def save(self, path):
        with open(path, "w+") as f:
            f.write(self.assemble())

    def add_body_line(self, text=""):
        if text:
            self.body += text + "\n"

    def add_divider(self):
        self.body += "===============================\n"
