from tag import Tag
from token import Token


class Lexer(object):
    def __init__(self, text: str):
        self.text = text
        self.position = 0

    def current(self):
        if self.position >= len(self.text):
            return '/0'
        return self.text[self.position]

    def next(self):
        self.position += 1

    def peek(self, symbol):
        self.next()
        return symbol == self.current()

    def nextToken(self):
        # <number>
        # +  - * / ( )
        # <whitespaces>
        if self.position >= len(self.text):
            return Token(Tag.EOF, self.position, '\0', None)
        if self.current() == ' ' or self.current() == '\t':
            while self.current() == ' ' or self.current() == '/t':
                self.next()

        if self.current().isdigit():
            num = 0
            start = self.position
            while self.current().isdigit():
                num = num * 10 + int(self.current())
                self.next()

            length = self.position - start
            text = self.text[start:start + length]
            # value = int(text)
            value = num
            return Token(Tag.NUM, start, text, value)

        if self.current().isalpha():
            text = ""
            start = self.position
            while self.current().isalnum():
                self.next()
            length = self.position - start
            text = self.text[start:start + length]
            kind = Tag.get_keyword_kind(text)
            return Token(kind, start, text, text)


        if self.current() == '+':
            position = self.position
            self.next()
            return Token(Tag.PLUS, position, '+', None)
        elif self.current() == '-':
            position = self.position
            self.next()
            return Token(Tag.MINUS, position, '-', None)
        elif self.current() == '*':
            position = self.position
            self.next()
            return Token(Tag.STAR, position, '*', None)
        elif self.current() == '/':
            position = self.position
            self.next()
            return Token(Tag.SLASH, position, '/', None)
        elif self.current() == '(':
            position = self.position
            self.next()
            return Token(Tag.OPENPARENTHESIS, position, '(', None)
        elif self.current() == ')':
            position = self.position
            self.next()
            return Token(Tag.CLOSEPARENTHESIS, position, ')', None)
        else:
            position = self.position
            self.next()
            return Token(Tag.BAD, position, self.text[position], None)



