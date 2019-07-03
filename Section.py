class Section:
    def __init__(self, name):
        self.name = name
        self.notes = []

    def add_note(self, note):
        self.notes.append(note)

    def del_note(self, note_name):
        for n in self.notes:
            if n.name == note_name:
                self.notes.remove(n)
