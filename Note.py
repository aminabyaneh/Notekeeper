class Note:
    def __init__(self, uid, data):
        self.uid = uid
        self.data = data

    def edit(self, data):
        self.data = data