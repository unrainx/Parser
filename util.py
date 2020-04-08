class Error(ValueError):
    ...


class Stack(object):
    def __init__(self):
        self.container = []

    def empty(self) -> bool:
        return len(self.container) == 0

    def top(self):
        if not self.empty():
            return self.container[-1]

    def pop(self):
        if not self.empty():
            self.container.pop(-1)

    def push(self, element):
        self.container.append(element)
