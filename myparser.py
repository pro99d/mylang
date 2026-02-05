from ast import arg
from ml_lexer import MyLangLexer
from dataclasses import dataclass
from typing import Any
from exceptions import RED, CLEAR
from ml_interpreter import MyLangInterpreter
import traceback

DEBUG = True # TODO change to False

@dataclass
class Token:
    type: str
    value: Any

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
        self.pos = 1
        self.file = file
    def print_call_stack(self):
        if not DEBUG:
            return
        l = list(traceback.format_stack(limit= 6))
        for call in l[:4]:
            print(call)

    def write_error(self, message, errcode= 1):
        token = self.tokens[self.pos - 1]
        with open(self.file) as f:
            errl = f.read().split("\n")[token.lineno-1]
        linen = f"{token.lineno}| "
        left = errl[:token.index]
        center = errl[token.index:token.end+1]
        end = errl[token.end+1:]
        shift = len(linen)
        shift_line = ' ' * (len(left) + shift)
        self.print_call_stack()
        print(f"{linen}{left}{RED}{center}{CLEAR}{end}")
        print(f"{shift_line}{RED}{'^'*(len(center))}{CLEAR}")
        print(f"{message} at line {token.lineno}") 
        if errcode != None:
            exit(errcode)

    def consume(self, expected_type):
        if self.pos < len(self.tokens) and self.tokens[self.pos].type == expected_type:
            self.pos += 1
            return self.tokens[self.pos - 1]
        else:
            self.write_error(f"Expected {expected_type}, got {self.tokens[self.pos].type}")

    def lookahead(self, dp: int= 0):
        if self.pos + dp < len(self.tokens):
            return self.tokens[self.pos + dp]
        else:
            return Token("EOF", None)

    def call_statement(self):
        name = self.tokens[self.pos-1]
        self.consume('LPAREN')
        self.pos += 1
        if self.lookahead(-1).type != "RPAREN":
            args = self.arguments()
        else:
            args = []
        self.pos -= 1
        self.consume('RPAREN')
        return AstNode("CALL", name.value, args)

    def arguments(self):
        token = self.tokens[self.pos-1]
        arguments = []
        expr = self.expression()
        arguments.append(expr)
        # self.write_error("", None)
        while self.pos < len(self.tokens):
            # token = self.tokens[self.pos-1]
            if self.lookahead().type != "COMMA":
                break
            else:
                self.consume("COMMA")
            arguments.append(self.expression())
        # print(arguments)
        return arguments
    def expression(self):
        left = self.term()
        # self.pos += 1
        if self.pos < len(self.tokens) and self.tokens[self.pos].type == 'LPAREN':
            call =  self.call_statement()
            self.pos += 1
            return call
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
            self.pos += 1
            right = self.term()
            left = AstNode(op, left, right, other)
        self.pos += 1
        return left

    def term(self):
        token = self.tokens[self.pos-1]
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
            # raise SyntaxError("Invalid syntax")
            self.write_error("Invalid syntax")

    def assignment(self):
        self.consume('ID')
        var_name = self.consume('ID')
        self.consume('ASSIGN')
        self.pos += 1
        expr = self.expression()
        self.pos -= 1
        self.consume('SEMI')
        self.pos += 1
        return AstNode("ASSIGN", var_name.value, expr)

    def func_args(self):
        token = self.lookahead()
        if token.type == "RPAREN":
            return []
        arguments = []
        expr = AstNode("READ", self.consume("ID").value)
        arguments.append(expr)
        while self.pos < len(self.tokens):
            # token = self.tokens[self.pos-1]
            if self.lookahead().type != "COMMA":
                break
            else:
                self.consume("COMMA")
            arguments.append(AstNode("READ", self.consume("ID").value))
        # self.pos -=1
        return arguments

    def function(self):
        self.consume("FUNC")
        name = self.consume("ID")
        # print(self.tokens[self.pos].type)
        self.consume("LPAREN") 
        arguments = self.func_args()
        self.consume("RPAREN")
        self.consume("LBRACE")
        instructions = []
        self.pos += 1
        while self.lookahead().type != "RBRACE":
            instructions.append(self.statement())
        r = self.consume("RBRACE")
        self.pos += 1
        return AstNode("FUNC", name.value, {"type":"ml", "call":instructions, "args":arguments})
    
    def return_sttmnt(self):
        self.pos -= 1
        self.consume("RETURN")
        self.pos += 1 #???
        if self.lookahead() != "SEMI":
            val = self.expression()
        else:
            val = AstNode("NOP", None)
        return AstNode("RETURN", val)

    def statement(self):
        token = self.tokens[self.pos-1]
        lookahead = self.lookahead()
        # print(self.lookahead())
        if token.type == 'ID' and token.value == 'var':
            self.pos -= 1
            return self.assignment()
        elif token.type == 'ID' and lookahead.type == "LPAREN":
            call = self.call_statement()
            self.consume("SEMI")
            return call
        elif token.type == "LPAREN":
            return self.expression()
        elif token.type == "RETURN":
            return self.return_sttmnt()
        # elif token.type == 'IF':
        #     self.pos -= 1
        #     return self.function()
        # elif token.type == 'WHILE':
        #     self.pos -= 1
        #     return self.function()
        elif token.type == 'FUNC':
            self.pos -= 1
            return self.function()
        # elif lookahead.type == "OP":
        #     return self.expression()
        else:
            print(token)
            self.write_error("Unknown statement")

    def parse(self):
        statements = []
        while self.pos < len(self.tokens):
            if self.tokens[self.pos-1].type == 'NEWLINE':
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
