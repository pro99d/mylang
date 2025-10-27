from sly import Parser
from lexer import MyLangLexer


my_lang_functions = {}


def ml_function(function):
    my_lang_functions[function.__name__[:-1]] = function
    return function


@ml_function
def print_(*args, **kargs):
    print(*args, **kargs)


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

    @_('STRING')
    def factor(self, p):
        return str(p.STRING)[1:-1]

    @_('LPAREN expr RPAREN')
    def factor(self, p):
        print("PARENS")
        return p.expr

    @_('ID LPAREN args RPAREN')
    def term(self, p):
        func = my_lang_functions.get(p.ID)
        if not func:
            raise NameError(f"Function {p.ID} is not defined!")
        return func(*p.args)

    @_('expr')
    def args(self, p):
        return p.expr

    @_('args COMMA expr')
    def args(self, p):
        return p.args+[p.expr.__repr__()]

    @_('expr COMMA expr')
    def args(self, p):
        return [p.expr0.__repr__(), p.expr1.__repr__()]

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
