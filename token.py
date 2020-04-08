

class Token(object):
    def __init__(self, kind, position: int, text: str, value):
        self.kind = kind
        self.position = position
        self.text = text
        self.value = value

    def __repr__(self):
        return "{}".format(self.text)
