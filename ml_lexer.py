from sly import Lexer
from sys import argv


class MyLangLexer(Lexer):
    tokens = {ID, NUMBER, ASSIGN, LPAREN, RPAREN, ASSIGN,
              STRING, SEMI, COMMA, IF, ELSE, LBRACE, RBRACE,
              WHILE, CONTINUE, BREAK, FUNC, RETURN, DOT,
              LSQBRACK, RSQBRACK, INC, DOLL, NOT, AND, OR, OP}
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
    ID["include"] = INC
    ID["not"] = NOT
    ID["and"] = AND
    ID["or"] = OR 
    DOT = r'\.'
    LBRACE = r'{'
    RBRACE = r'}'
    DOLL = r'\$'
    LSQBRACK = r'\['
    RSQBRACK = r'\]'

    # Longer operators first to ensure proper matching
    OP =  r'(>=|<=|>|<|\+|-|\*|/|==)'
    ASSIGN = r'='
    LPAREN = r'\('
    RPAREN = r'\)'
    SEMI = r';'
    # COLON = r':'
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
