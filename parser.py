from exceptions import RED, CLEAR
import sys
import os
stderr = sys.stderr
sys.stderr = open(os.devnull, "w")
from sly import Parser
from lexer import MyLangLexer
DEBUG = True
sys.stderr = stderr

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


class MyLangParser(Parser):
    tokens = MyLangLexer.tokens

    def __init__(self):
        self.names = ml_globals

        # super().log = MyLangLogger(sys.stderr)
    start = 'statements'

    @_('statement')
    def statements(self, p):
        return p.statement

    @_('statements SEMI statement')
    def statements(self, p):
        return p.statement

    @_('statements SEMI')
    def statements(self, p):
        return p.statements

    @_('ID ASSIGN expr')
    def statement(self, p):
        self.names[p.ID] = p.expr
        return p.expr

    # @_('ID LPAREN ARG')

    @_('expr')
    def statement(self, p):
        return p.expr

    @_('expr PLUS term')
    def expr(self, p):
        return p.expr + p.term

    @_('expr MINUS term')
    def expr(self, p):
        return p.expr - p.term

    @_('term')
    def expr(self, p):
        return p.term

    @_('term TIMES factor')
    def term(self, p):
        return p.term * p.factor

    @_('term DIVIDE factor')
    def term(self, p):
        return p.term / p.factor

    @_('factor')
    def term(self, p):
        return p.factor

    @_('NUMBER')
    def factor(self, p):
        return p.NUMBER
    # @_('NUMBER DOT NUMBER')
    # def factor(self, p):
    #     return float(f"{p.NUMBER0}.{p.NUMBER1}")

    @_('STRING')
    def factor(self, p):
        return str(p.STRING)[1:-1]

    @_('LPAREN expr RPAREN')
    def factor(self, p):
        print("PARENS")
        return p.expr

    @_('ID LPAREN args RPAREN')
    def term(self, p):
        func = self.names.get(p.ID)
        if not func:
            raise NameError(f"{RED}Function {p.ID} is not defined!{CLEAR}")
        if not isinstance(p.args, list):
            args = [p.args]
        else:
            args = p.args
        return func(*args)

    @_('expr')
    def args(self, p):
        return p.expr

    @_('args COMMA expr')
    def args(self, p):
        return p.args+[p.expr]

    @_('expr COMMA expr')
    def args(self, p):
        return [p.expr0, p.expr1]

    @_('ID')
    def factor(self, p):
        if p.ID in self.names:
            return self.names[p.ID]
        else:
            raise NameError(f"Name '{p.ID}' is not defined")


if __name__ == '__main__':
    lexer = MyLangLexer()
    parser = MyLangParser()
    text = open("./simple.mylang").read()
    if text:
        tokens = lexer.tokenize(text)
        try:
            result = parser.parse(tokens)
            # print(parser.names)
        except NameError as e:
            print(f"Error: {e}")
    else:
        pass
