from collections import deque


class HistoryObject:
    __slots__ = ["id", "data"]

    def __init__(self, id, data):
        self.id = str(id)
        self.data = data

    def __str__(self):
        return self.id

    def __repr__(self):
        return self.id


class HistoryMixin:
    def __init__(self, data):
        self.history = deque()
        self.history_index = 0
        self.history.append(HistoryObject(0, data))
        self.history_uid = 1

    def get_uid(self):  # Return UID and increment by 1
        self.history_uid += 1
        return self.history_uid - 1

    def add_history(self, data):
        id = self.get_uid()
        while self.history_index < len(self.history) - 1:
            self.history.pop()  # Clear old timeline
        self.history.append(HistoryObject(id, data))
        self.history_index = len(self.history) - 1

    def undo(self):
        if self.history_index > 0:
            self.history_index -= 1
        print(f"Loading History {self.history[self.history_index].id}")
        return self.history[self.history_index].data

    def redo(self):
        if self.history_index == len(self.history) - 1:
            return
        self.history_index += 1
        return self.history[self.history_index].data

    def clear_history(self, data):
        self.history = deque()
        self.history_index = 0
        self.history.append(HistoryObject(0, data))
        self.history_uid = 1
