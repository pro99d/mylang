from sly import Parser
from lexer import MyLangLexer
import os
import sys


class MyLangParser(Parser):
    tokens = MyLangLexer.tokens

    def __init__(self):
        self.names = {}

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

    # @_('expr')
    # def statement(self, p):
    #     return p.expr

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

    @_('STRING')
    def factor(self, p):
        return str(p.STRING)[1:-1]

    @_('LPAREN expr RPAREN')
    def factor(self, p):
        return p.expr

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
            print(parser.names)
        except NameError as e:
            print(f"Error: {e}")
    else:
        pass
