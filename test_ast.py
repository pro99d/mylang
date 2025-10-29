from exceptions import RED, CLEAR
import sys
import os
# stderr = sys.stderr
# sys.stderr = open(os.devnull, "w")
from sly import Parser
from lexer import MyLangLexer
DEBUG = True
# sys.stderr = stderr

ml_globals = {}


def ml_function(function):
    ml_globals[function.__name__[:-1]] = function
    return function


@ml_function
def print_(*args, **kargs):
    print(*args, **kargs)


@ml_function
def type_(*args, **kargs):
    return type(*args, **kargs)

class AstNode:
    def __init__(self, op, left, right=None):
        self.op = op 
        self.l = left 
        self.r = right
    def __repr__(self):
        return f"({self.op}, {self.l}, {self.r})"

class Interpreter:
    def __init__(self):
        pass
    def interpret(self, data: AstNode):
        op = data.op 
        left = data.l 
        right = data.r
        i = self.interpret
        match op:
            case "NUMBER":
                return left
            case "ASSIGN":
                ml_globals[left] = i(right)
                return i(right)
            case "READ":
                if left in ml_globals:
                    return ml_globals[left]
                else:
                    raise NameError(f"Undefined name {left}")
            case "ADD":
                return i(left)+i(right)
            case "SUB":
                return i(left)-i(right)
            case "MUL":
                return i(left)*i(right)
            case "DIV":
                return i(left)/i(right)
            case _:
                print(f"Unknown operation {op}")
                return


class MyLangParser(Parser):
    tokens = MyLangLexer.tokens

    def __init__(self):
        self.names = ml_globals

    @_('ID ASSIGN expr')
    def expr(self, p):
        # self.names[p.ID] = p.expr
        return AstNode("ASSIGN", p.ID, p.expr)

    # @_('ID LPAREN ARG')

    # @_('expr')
    # def statement(self, p):
    #     return p.expr

    @_('expr PLUS term')
    def expr(self, p):
        return AstNode("ADD", p.expr, p.term)

    @_('expr MINUS term')
    def expr(self, p):
        return AstNode("SUB", p.expr, p.term)

    @_('term')
    def expr(self, p):
        return p.term

    @_('term TIMES factor')
    def term(self, p):
        return AstNode("MUL", p.term, p.factor)

    @_('term DIVIDE factor')
    def term(self, p):
        return AstNode("DIV", p.term, p.factor)

    @_('factor')
    def term(self, p):
        return p.factor

    @_('NUMBER')
    def factor(self, p):
        return AstNode("NUMBER", p.NUMBER)


    @_('LPAREN expr RPAREN')
    def factor(self, p):
        print("PARENS")
        return AstNode("NUMBER", p.expr)

    @_('ID')
    def factor(self, p):
        return AstNode("READ", p.ID)


if __name__ == '__main__':
    lexer = MyLangLexer()
    parser = MyLangParser()
    interpreter = Interpreter()
    while True:
        text = input("mylang > ")
        if text:
            tokens = lexer.tokenize(text)
            try:
                result = parser.parse(tokens)
                print(result)
                result = interpreter.interpret(result)
                print(result)
            except NameError as e:
                print(f"Error: {e}")
        else:
            break 

