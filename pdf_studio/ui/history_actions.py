class HistoryActions:
    def undo(self):
        self.history.undo()
        self.refresh()

    def redo(self):
        self.history.redo()
        self.refresh()
