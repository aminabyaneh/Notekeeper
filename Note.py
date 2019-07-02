class Note:
    def __init__(self, name, data):
        self.name = name
        self.data = data

    def edit(self, data):
        self.data = data
