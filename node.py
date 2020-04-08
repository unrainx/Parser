from tag import Tag
from token import Token

class Node(object):
    # def __int__(self, kind):
    #     self.kind = kind
    ...


class Expression(Node):
    def __init__(self, kind):
        self.kind = kind


class Number(Expression):
    def __init__(self, number_token):
        super(Number, self).__init__(Tag.NUM)
        self.number_token = number_token

    def __repr__(self):
        return "{}".format(self.number_token.value)


class BinaryExpression(Expression):
    def __init__(self, lhs, op, rhs):
        super(BinaryExpression, self).__init__(Tag.BinaryExpression)
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

    def __repr__(self):
        return "{} {} {}".format(self.lhs, self.op, self.rhs)


class UnaryExpression(Expression):
    def __init__(self, operator, operand):
        super(UnaryExpression, self).__init__(Tag.UnaryExpression)
        self.operator = operator
        self.operand = operand

    def __repr__(self):
        return "{}{}".format(self.operator, self.operand)


class LiteralExpression(Expression):
    def __init__(self, value):
        super(LiteralExpression, self).__init__(Tag.Literal)
        self.value = value

    def __repr__(self):
        return "{}".format(self.value)


class ParenthesziedExpression(Expression):
    def __init__(self, open_parenthesis: Token, expr: Expression, close_parenthesis: Token):
        super(ParenthesziedExpression, self).__init__(Tag.PARENTHESISEXPRESSION)
        self.open_parenthesis = open_parenthesis
        self.expr = expr
        self.close_parenthesis = close_parenthesis

    def __repr__(self):
        return "{} {} {}".format(self.open_parenthesis, self.expr, self.close_parenthesis)


class Ast(object):
    def __init__(self, diagnostic, root, eof_token):
        self.diagnostic = diagnostic
        self.root = root
        self.eof_token = eof_token

    def __repr__(self):
        return str(self.diagnostic)

