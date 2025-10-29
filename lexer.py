from sly import Lexer


class MyLangLexer(Lexer):
    tokens = {ID, COMPARE, NUMBER, PLUS, MINUS, TIMES,
              DIVIDE, ASSIGN, LPAREN, RPAREN,
              LBRACE, RBRACE, STRING, SEMI, COMMA}

    ignore = ' \t'
    ignore_comments = r"\#.*"
    # ignore_separator = r';'
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    COMPARE = r'=='
    ASSIGN = r'='
    LPAREN = r'\('
    RPAREN = r'\)'
    SEMI = r';'
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
    data = open("./simple.mylang").read()
    lexer = MyLangLexer()
    for tok in lexer.tokenize(data):
        print('type=%r, value=%r' % (tok.type, tok.value))
