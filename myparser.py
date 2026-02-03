from ml_lexer import MyLangLexer
from dataclasses import dataclass
from typing import Any
from exceptions import RED, CLEAR
from ml_interpreter import MyLangInterpreter


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
    def __repr__(self):
        return f"AstNode(op={self.op}, left={self.l}, right={self.r}, other={self.other})"

class Parser:
    def __init__(self, tokens, file):
        self.tokens = tokens
        self.pos = 0
        self.file = file
    def write_error(self, message, errcode= 1):
        token = self.tokens[self.pos]
        with open(self.file) as f:
            errl = f"{token.lineno}| {f.readline()}"
        left = errl[:token.index]
        center = errl[token.index:token.end+1]
        end = errl[token.end+1:]
        print(f"{left}{RED}{center}{CLEAR}{end[:-1]}")
        print(f"{' '*(1+token.index)}{RED}{'^'*(len(center)-1)}{CLEAR}")
        print(f"{message} at line {self.tokens[self.pos-1].lineno}") 
        if errcode != None:
            exit(errcode)

    def consume(self, expected_type):
        if self.pos < len(self.tokens) and self.tokens[self.pos].type == expected_type:
            self.pos += 1
            return self.tokens[self.pos - 1]
        else:
            raise SyntaxError(
                f"Expected {expected_type}, got {self.tokens[self.pos].type}")

    def lookahead(self, dp: int= 1):
        if self.pos + dp < len(self.tokens):
            return self.tokens[self.pos + dp]

    def call_statement(self):
        name = self.consume('ID')
        self.consume('LPAREN')
        args = self.arguments()
        self.consume('RPAREN')
        self.consume('SEMI')
        return AstNode("CALL", name.value, args)

    def arguments(self):
        token = self.tokens[self.pos]
        arguments = []
        expr = self.expression()
        arguments.append(expr)
        # self.write_error("", None)
        while self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            arguments.append(self.expression())
            if self.lookahead().type != "COMMA":
                break
            else:
                self.consume("COMMA")
            # self.pos += 1
        return arguments
    def expression(self):
        left = self.term()
        self.pos += 1
        while self.pos < len(self.tokens) and self.tokens[self.pos].type == 'OP':
            op = self.consume('OP')
            other = []
            match op.value:
                case "+":
                    op = "ADD"
                case "-":
                    op = "SUB"
                case "/":
                    op = "DIV"
                case "*":
                    op = "MUL"
                case _:
                    if op in [">=", "<=", "==", "<", ">"]:
                        other.append(op)
                        op = 'cond'
            right = self.term()
            left = AstNode(op, left, right, other)
        return left

    def term(self):
        token = self.tokens[self.pos]
        if token.type == 'NUMBER':
            num = token.value
            return AstNode("NUMBER", num)
        elif token.type == 'STRING':
            return AstNode("STRING", token.value)
        elif token.type == 'ID':
            id = token.value
            return AstNode("READ", id)
        elif token.type == 'LPAREN':
            self.consume('LPAREN')
            expr = self.expression()
            self.consume('RPAREN')
            return expr
        else:
            print(token)
            raise SyntaxError("Invalid syntax")
            # self.write_error("Invalid syntax")

    def assignment(self):
        self.consume('ID')
        var_name = self.consume('ID')
        self.consume('ASSIGN')
        expr = self.expression()
        self.consume('SEMI')
        return AstNode("ASSIGN", var_name.value, expr)

    def statement(self):
        token = self.tokens[self.pos]
        if token.type == 'ID' and token.value == 'var':
            return self.assignment()
        elif token.type == 'ID' and self.lookahead().type == "LPAREN":
            return self.call_statement()
        elif self.lookahead(2).type == "OP":
            return self.expression()
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
    interpreter = MyLangInterpreter()
    with open("test.par") as f:
        file = f.read()
    lexed = list(lexer.tokenize(file))
    parser = Parser(lexed, "test.par")
    parsed = parser.parse()
    print(parsed)
    for statement in parsed:
        interpreter.interpret(statement)


if __name__ == "__main__":
    main()
