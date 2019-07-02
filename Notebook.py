class Notebook:
    def __init__(self, username=None):
        self.username = username
        self.sections = []

    def add_section(self, section):
        self.sections.append(section)

    def remove_section(self, section_name):
        for s in self.sections:
            if s.name == section_name:
                self.sections.remove(s)
