from collections import deque


class HistoryObject:
    """Basic object to hold history data"""

    __desc__ = """This object is not meant to be instantiated directly usually. \
It is used by the HistoryMixin class to track one instance of an application's \
history. It may be useful to subclass this object as well as the HistoryMixin \
object to make a more complicated history tracking system."""
    
    __slots__ = ["id", "data"]

    def __init__(self, id, data):
        self.id = str(id)
        self.data = data

    def __str__(self):
        return self.id

    def __repr__(self):
        return self.id


class HistoryMixin:
    """Abstract mixin to add history-tracking to an application"""

    __desc__ = """This object is meant to be used as a mixin rather than \
instantiated directly most of the time."""
    
    __slots__ = ["history", "history_index", "history_uid"]

    def __init__(self, data):
        self.history = deque()
        self.history_index = 0
        self.history.append(HistoryObject(0, data))
        self.history_uid = 1

    def get_history_uid(self):  # Return UID and increment by 1
        self.history_uid += 1
        return self.history_uid - 1

    def add_history(self, data):
        id = self.get_history_uid()
        print(f"Adding History with id {id}")
        while self.history_index < len(self.history) - 1:
            self.history.pop()  # Clear old timeline
        self.history.append(_HistoryObject(id, data))
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
