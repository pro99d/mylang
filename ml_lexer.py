from sly import Lexer
from sys import argv


class MyLangLexer(Lexer):
    tokens = {ID, COMPARE, NUMBER, PLUS, MINUS, TIMES,
              DIVIDE, ASSIGN, LPAREN, RPAREN,
              STRING, SEMI, COMMA, IF, ELSE, #FUNC,
              GOE, SOE, GREATER, SMALLER, LBRACE, RBRACE,
              WHILE, CONTINUE, BREAK, FUNC, RETURN, DOT,
              COLON}
    ignore = ' \t'
    ignore_comments = r"\#.*"
    # ignore_separator = r';'
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    
    ID['if'] = IF
    ID['else'] = ELSE
    # ID['func'] = FUNC
    ID['while'] = WHILE
    ID['break'] = BREAK
    ID['continue'] = CONTINUE
    ID["return"] = RETURN
    ID["func"] = FUNC
    DOT = r'\.'
    LBRACE = r'{'
    RBRACE = r'}'

    GOE = r'>='
    SOE = r'<='
    GREATER = r'>'
    SMALLER = r'<'
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    COMPARE = r'=='
    ASSIGN = r'='
    LPAREN = r'\('
    RPAREN = r'\)'
    SEMI = r';'
    COLON = r':'
    COMMA = r','
    # DOT = r'.'

    @_(r'\n+')
    def newline(self, t):
        self.lineno += len(t.value)

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r'"[^"]*"')
    def STRING(self, t):
        t.value = t.value[1:-1]
        return t


if __name__ == '__main__':
    if len(argv) > 1:
        name = argv[1]
    else:
        name = "function.mylang"
    data = open(name).read()
    lexer = MyLangLexer()
    for tok in lexer.tokenize(data):
        print('type=%r, value=%r' % (tok.type, tok.value))
