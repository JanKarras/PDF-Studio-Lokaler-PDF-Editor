class History:
    """Reference snapshots; no PDF bytes are copied by editing commands."""

    def __init__(self):
        self.pages = ()
        self.past = []
        self.future = []
        self.saved = ()
        self.limit = 100

    def commit(self, pages, label):
        pages = tuple(pages)
        if pages == self.pages:
            return False
        self.past.append((self.pages, label))
        self.past = self.past[-self.limit:]
        self.pages = pages
        self.future.clear()
        return True

    def undo(self):
        if self.past:
            pages, label = self.past.pop()
            self.future.append((self.pages, label))
            self.pages = pages

    def redo(self):
        if self.future:
            pages, label = self.future.pop()
            self.past.append((self.pages, label))
            self.pages = pages
