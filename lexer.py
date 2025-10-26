from sly import Lexer

class MyLangLexer(Lexer):
    tokens = { ID, NUMBER, PLUS, MINUS, TIMES,
               DIVIDE, ASSIGN, LPAREN, RPAREN,
              LBRACE, RBRACE, STRING, SEMI, COMMA}
    literals = {'(', ")", '{', "}"}
    # String containing ignored characters between tokens
    ignore = ' \t'
    ignore_comments = r"\#.*"
    ignore_newline = r'\n+'
    # ignore_separator = r';'
    # Regular expression rules for tokens
    ID = r'[a-zA-Z_][a-zA-Z_]*'
    STRING = r'"[a-zA-Z_][a-zA-Z0-9_]*"'
    NUMBER  = r'\d+'
    PLUS    = r'\+'
    MINUS   = r'-'
    TIMES   = r'\*'
    DIVIDE  = r'/'
    ASSIGN  = r'='
    LPAREN  = r'\('
    RPAREN  = r'\)'
    SEMI = r';'

    LBRACE = r'\{'
    RBRACE = r'\}'
    
    COMMA = r'\,'
    
    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)   # Convert to a numeric value
        return t
    
    @_(r'"[^"]*"')
    def STRING(self, t):
        t.value = str(t.value)[1:-1]
        return t

if __name__ == '__main__':
    data = open("./simple.mylang").read()
    lexer = MyLangLexer()
    for tok in lexer.tokenize(data):
        print('type=%r, value=%r' % (tok.type, tok.value))
