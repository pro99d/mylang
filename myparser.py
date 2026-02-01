from ml_lexer import MyLangLexer
from dataclasses import dataclass
from typing import Any


class TokenType:
    number = "NUMBER"


class ASTNode:
    pass


@dataclass
class Number(ASTNode):
    number: float
    def __call__(self):
        return self.number


@dataclass
class BinOp(ASTNode):
    left: Any
    op: str
    right: Any


@dataclass
class Variable(ASTNode):
    name: str


@dataclass
class Assign(ASTNode):
    name: str
    value: Any


@dataclass
class Call(ASTNode):
    name: str
    arg: list


class AstNode:
    def __init__(self, op, left, right=None, other=[]):
        self.op = op
        self.l = left
        self.r = right
        self.other = other

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def consume(self, expected_type):
        if self.pos < len(self.tokens) and self.tokens[self.pos].type == expected_type:
            self.pos += 1
            return self.tokens[self.pos - 1]
        else:
            raise SyntaxError(
                f"Expected {expected_type}, got {self.tokens[self.pos-1]}")

    def lookahead(self):
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1]

    def call_statement(self):
        name = self.consume('ID')
        self.consume('LPAREN')
        args = self.arguments()
        self.consume('RPAREN')
        self.consume('SEMI')
        return AstNode("CALL", name, args)
        return Call(name, args)

    def arguments(self):
        token = self.tokens[self.pos]
        arguments = []
        if token.type in ('STRING', 'NUMBER', 'ID'):
            arguments.append(token.value)
            self.pos += 1
        else:
            raise SyntaxError(f"Invalid syntax at line {token.lineno}")

        while self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            if token.type in ('STRING', 'NUMBER', 'ID'):
                arguments.append(token.value)
            if self.lookahead() != "SEMI":
                break
            else:
                self.consume("SEMI")
            self.pos += 1
        return arguments
    def expression(self):
        left = self.term()
        while self.pos < len(self.tokens) and self.tokens[self.pos] == 'OP':
            op = self.consume('OP')
            right = self.term()
            left = BinOp(left, op, right)
        return left

    def term(self):
        token = self.tokens[self.pos]
        if token.type == 'NUMBER':
            return AstNode("NUMBER", self.consume('NUMBER'))
        elif token.type == 'ID':
            return Variable(self.consume('ID'))
        elif token.type == 'LPAREN':
            self.consume('LPAREN')
            expr = self.expression()
            self.consume('RPAREN')
            return expr
        else:
            raise SyntaxError("Invalid syntax")

    def assignment(self):
        self.consume('ID')  # consume 'let'
        var_name = self.consume('ID')
        self.consume('ASSIGN')
        expr = self.expression()
        self.consume('SEMI')
        return Assign(var_name, expr)

    def statement(self):
        token = self.tokens[self.pos]
        if token.type == 'ID' and token.value == 'var':
            return self.assignment()
        elif token.type == 'ID' and self.lookahead().type == "LPAREN":
            return self.call_statement()
        else:
            raise SyntaxError("Unknown statement")

    def parse(self):
        statements = []
        while self.pos < len(self.tokens):
            if self.tokens[self.pos].type == 'NEWLINE':
                self.pos += 1  # Skip newlines
                continue
            statements.append(self.statement())
        return statements


def main():
    lexer = MyLangLexer()
    with open("test.par") as f:
        file = f.read()
    lexed = list(lexer.tokenize(file))
    parser = Parser(lexed)
    print(parser.parse())


if __name__ == "__main__":
    main()
