from enum import Enum


class Tag(Enum):
    # token
    NUM = 257
    PLUS = 258
    MINUS = 259
    STAR = 260
    SLASH = 261
    OPENPARENTHESIS = 262
    CLOSEPARENTHESIS = 263
    BAD = 264
    EOF = 265

    # expressions
    BinaryExpression = 266
    PARENTHESISEXPRESSION = 267
    Number = 268
    Literal = 269
    UnaryExpression = 270

    # keywords
    TrueKeyWord = 271
    FalseKeyWord = 27

    # identifier
    IdentifierToken = 273

    @staticmethod
    def get_keyword_kind(text: str):
        if text == "true":
            return Tag.TrueKeyWord
        elif text == "false":
            return Tag.FalseKeyWord
        else:
            return Tag.IdentifierToken
