"""
todo: 
 [ ] - задокументировать ошибки  и предупреждения в SLY 
"""

from exceptions import RED, CLEAR
import sys
import os
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
    def __init__(self, op, left, right=None):
        self.op = op 
        self.l = left 
        self.r = right
    def __repr__(self):
        return f"({self.op}, {self.l}, {self.r})"



class MyLangParser(Parser):
    tokens = MyLangLexer.tokens

    def __init__(self):
        super().__init__()
        self.names = ml_globals

        # super().log = MyLangLogger(sys.stderr)
    start = 'statements'

    @_('statement')
    def statements(self, p):
        return [p.statement]

    @_('statements SEMI statement')
    def statements(self, p):
        return p.statements+[p.statement]

    @_('statements SEMI')
    def statements(self, p):
        return p.statements

    @_('ID ASSIGN expr')
    def statement(self, p):
        # self.names[p.ID] = p.expr
        return AstNode("ASSIGN", p.ID, p.expr)
    
    # @_('ID LPAREN ARG')

    @_('expr')
    def statement(self, p):
        return p.expr

    @_('expr PLUS term')
    def expr(self, p):
        return AstNode("ADD", p.expr, p.term)

    @_('expr MINUS term')
    def expr(self, p):
        return AstNode("SUB", p.expr, p.term)

    @_('term')
    def expr(self, p):
        return p.term

    @_('term COMPARE factor')
    def term(self, p):
        return AstNode("COMPARE", p.term, p.factor)
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
        return AstNode("STRING", str(p.STRING)[1:-1])

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
        return AstNode("READ", p.ID)


if __name__ == '__main__':
    lexer = MyLangLexer()
    parser = MyLangParser()
    interpreter = MyLangInterpreter()
    # while True:
    text = open("./simple.mylang").read()
    if text:
        # for i in text.split("\n"):
        tokens = lexer.tokenize(text)
        try:
            result = parser.parse(tokens)
            for statement in result:
                interpreter.interpret(statement)
            # print(result)
            # print(parser.names)
        except NameError as e:
            print(f"Error: {e}")
    else:
        pass
