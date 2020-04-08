# import abc
from util import Error
from lexer import Lexer
from node import *


class Parser(object):
    def __init__(self, text: str):
        self.lexer = Lexer(text)
        self.position = 0
        self.tokens = []
        token = self.lexer.nextToken()
        while token.kind != Tag.EOF:
            self.tokens.append(token)
            token = self.lexer.nextToken()

    def peek(self, offset):
        index = self.position + offset
        if index >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[index]

    def current(self):
        return self.peek(0)

    def move(self):
        current = self.current()
        self.position += 1
        return current

    def match(self, kind):
        if self.current().kind == kind:
            return self.move()
        return Token(kind, self.current().position, "", None)

    @staticmethod
    def get_binary_operator_precedence(kind):
        precedence = {
            Tag.PLUS: 19,
            Tag.MINUS: 19,
            Tag.STAR: 20,
            Tag.SLASH: 20,
        }
        return precedence.get(kind, 0)

    def get_unary_operator_precedence(self, kind):
        precedence = {
            Tag.PLUS: 20,
            Tag.MINUS: 20,
        }
        return precedence.get(kind, 0)

    '''
    precedence:
        zuo jie he  + -
        zuo jie he  * /
        
    factor  ->  digit   
            |   (expr)
    term    ->  term    *   factor
            |   term    /   factor
            |   factor  
    expr    ->  expr    +   term
            |   expr    -   term
            |   term
    '''
    def parsePrimaryExpression(self):
        if self.current().kind == Tag.OPENPARENTHESIS:
            left = self.move()
            expr = self.parse_expression()
            right = self.match(Tag.CLOSEPARENTHESIS)
            return ParenthesziedExpression(left, expr, right)
        number_token = self.match(Tag.NUM)
        return Number(number_token)

    def parse_expression(self, parent_precedence=0):
        unary_operator_precedence = self.get_unary_operator_precedence(self.current().kind)
        if unary_operator_precedence != 0 and unary_operator_precedence >= parent_precedence:
            operator_token = self.move()
            operand = self.parse_expression(unary_operator_precedence)
            left = UnaryExpression(operator_token, operand)
        else:
            left = self.parsePrimaryExpression()
        while True:
            precedence = self.get_binary_operator_precedence(self.current().kind)
            if precedence == 0 or precedence <= parent_precedence:
                break
            operator_token = self.move()
            right = self.parse_expression(precedence)
            left = BinaryExpression(left, operator_token, right)

        return left

    def parse(self):
        expression = self.parse_expression()
        end_of_file_token = self.match(Tag.EOF)
        ast = Ast(expression, expression, end_of_file_token)
        return ast


class Evalutor(object):
    def __init__(self, root):
        self.root = root

    def evalutor(self) -> int:
        return self.evaluate_exp(self.root)

    def evaluate_exp(self, root) -> int:
        if root.kind == Tag.NUM:
            return root.number_token.value
        elif root.kind == Tag.PARENTHESISEXPRESSION:
            return self.evaluate_exp(root.expr)
        elif root.kind == Tag.UnaryExpression:
            operand = self.evaluate_exp(root.operand)
            if root.operator.kind == Tag.PLUS:
                return operand
            elif root.operator.kind == Tag.MINUS:
                return -operand
            else:
                raise Error("unexpected unary operator")
        elif root.kind == Tag.BinaryExpression:
            lhs = self.evaluate_exp(root.lhs)
            rhs = self.evaluate_exp(root.rhs)
            if root.op.kind == Tag.PLUS:
                return lhs + rhs
            elif root.op.kind == Tag.MINUS:
                return lhs - rhs
            elif root.op.kind == Tag.STAR:
                return lhs * rhs
            elif root.op.kind == Tag.SLASH:
                return lhs / rhs
            else:
                raise Error("op is invaild.")
        raise Error("node is invaild")


class TestUnit:
    def __init__(self):
        self.no = self.test_no()

    @staticmethod
    def test_no():
        n = 1
        while True:
            yield n
            n += 1

    def test(self, output, expect):
        print("result of test {} is : ".format(next(self.no)), output == expect)


def shell():
    while True:
        print(">", end=" ")
        cmd = input()
        print('\n')
        try:
            result = Evalutor(Parser(cmd).parse().root).evalutor()
            print("result: ", result)
        except:
            print("syntax error, please retry.")

if __name__ == '__main__':
    test = TestUnit()
    test.test(Evalutor(Parser("--1").parse().root).evalutor(), 1)
    test.test(Evalutor(Parser("-1").parse().root).evalutor(), -1)
    test.test(Evalutor(Parser("1 + 3 * 5").parse().root).evalutor(), 16)
    test.test(Evalutor(Parser("(1 + 3) * 5").parse().root).evalutor(), 20)
    shell()