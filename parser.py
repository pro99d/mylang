"""
todo: 
 [ ] - задокументировать ошибки  и предупреждения в SLY 
"""

from exceptions import RED, CLEAR
from sys import argv
# import os
from namespace import ml_globals
from interpreter import MyLangInterpreter
from sly import Parser
from lexer import MyLangLexer
DEBUG = True


# декоратор для добавления функции языку
def ml_function(function):
    ml_globals[function.__name__[:-1]] = function
    return function


class AstNode:
    def __init__(self, op, left, right=None, other=[]):
        self.op = op
        self.l = left
        self.r = right
        self.other = other

    def __repr__(self):
        return f"({self.op}, {self.l}, {self.r}, {self.other})"


class MyLangParser(Parser):
    tokens = MyLangLexer.tokens

    def __init__(self):
        super().__init__()
        self.names = ml_globals

        # super().log = MyLangLogger(sys.stderr)
    start = 'program'

    @_('statements')
    def program(self, p):
        return p.statements

    @_('')
    def statements(self, p):
        return []

    @_('statements statement')
    def statements(self, p):
        return p.statements + [p.statement]

    @_('IF LPAREN cond RPAREN LBRACE statements RBRACE else_')
    def statement(self, p):
        return AstNode("IF", p.cond, p.statements, other=[AstNode("ELSE", p.else_)])

    @_("WHILE LPAREN cond RPAREN LBRACE statements RBRACE")
    def statement(self, p):
        return AstNode("WHILE", p.cond, p.statements)

    @_('BREAK')
    def statement(self, p):
        return AstNode("BREAK", None)

    @_('CONTINUE')
    def statement(self, p):
        return AstNode("CONTINUE", None)

    @_('')
    def else_(self, p):
        return AstNode("ELSE", [AstNode("NOP", None)])

    @_('ELSE LBRACE statements RBRACE')
    def else_(self, p):
        return AstNode("ELSE", p.statements)
    # @_('IF LPAREN expr RPAREN LBRACE statements RBRACE')
    # def statement(self, p):
    #     return AstNode("IF", p.expr, p.statements)

    @_('statements SEMI statement')
    def statements(self, p):
        return p.statements+[p.statement]

    @_('ID ASSIGN expr')
    def statement(self, p):
        # self.names[p.ID] = p.expr
        return AstNode("ASSIGN", p.ID, p.expr)

    # @_('ID LPAREN ARG')

    @_('expr SEMI')
    def statement(self, p):
        return p.expr

    @_('expr PLUS term')
    def expr(self, p):
        return AstNode("ADD", p.expr, p.term)

    @_('expr MINUS term')
    def expr(self, p):
        return AstNode("SUB", p.expr, p.term)

    @_('term GOE factor')
    def cond(self, p):
        return AstNode("cond", p.term, p.factor, other=["GOE"])

    @_('term SOE factor')
    def cond(self, p):
        return AstNode("cond", p.term, p.factor, other=["SOE"])

    @_('term SMALLER factor')
    def cond(self, p):
        return AstNode("cond", p.term, p.factor, other=["SMALLER"])

    @_('term GREATER factor')
    def cond(self, p):
        return AstNode("cond", p.term, p.factor, other=["GREATER"])

    @_('term')
    def expr(self, p):
        return p.term

    @_('term COMPARE factor')
    def cond(self, p):
        return AstNode("cond", p.term, p.factor, other=["COMPARE"])

    @_('term TIMES factor')
    def term(self, p):
        return AstNode("TIMES", p.term, p.factor)

    @_('term DIVIDE factor')
    def term(self, p):
        return AstNode("DIVIDE", p.term, p.factor)

    @_('factor')
    def term(self, p):
        return p.factor

    @_('NUMBER')
    def factor(self, p):
        return AstNode("NUMBER", p.NUMBER)
    # @_('NUMBER DOT NUMBER')
    # def factor(self, p):
    #     return float(f"{p.NUMBER0}.{p.NUMBER1}")

    @_('STRING')
    def factor(self, p):
        return AstNode("STRING", str(p.STRING))

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
        return AstNode("CALL", func, args)

    @_('expr args_tail')
    def args(self, p):
        return [p.expr] + p.args_tail

    @_('')
    def args_tail(self, p):
        return []

    @_('COMMA expr args_tail')
    def args_tail(self, p):
        return [p.expr] + p.args_tail

    @_('ID')
    def factor(self, p):
        return AstNode("READ", p.ID, other= [p.lineno])


if __name__ == '__main__':
    lexer = MyLangLexer()
    parser = MyLangParser()
    interpreter = MyLangInterpreter()
    # while True:
    if len(argv) > 1:
        name = argv[1]
    else:
        name = "simple.mylang"
    text = open(name).read()
    if text:
        # for i in text.split("\n"):
        tokens = lexer.tokenize(text)
        try:
            result = parser.parse(tokens)
            print(result)
            for statement in result:
                interpreter.interpret(statement)
            # print(result)
            # print(parser.names)
        except NameError as e:
            print(f"Error: {e}")
    else:
        pass
