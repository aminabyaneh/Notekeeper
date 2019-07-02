class Section:
    def __init__(self, name):
        self.name = name
        self.notes = []

    def add_note(self, note):
        self.notes.append(note)

    def del_note(self, note_uid):
        for n in self.notes:
            if n.uid == note_uid:
                self.notes.remove(n)
