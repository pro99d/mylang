from lexer import MyLangLexer
from sly import Parser
from namespace import ml_globals
from exceptions import RED, CLEAR
from parser import ml_function

@ml_function
def print_(*args):
    print(*args)


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

    @_('IF LPAREN expr RPAREN LBRACE statements RBRACE')
    def statement(self, p):
        return AstNode("IF", p.expr, p.statements)

    # @_('IF LPAREN expr RPAREN LBRACE statements RBRACE')
    # def statement(self, p):
    #     return AstNode("IF", p.expr, p.statements)

    @_('statements SEMI statement')
    def statements(self, p):
        return p.statements+[p.statement]
    
    # @_('statements SEMI')
    # def statements(self, p):
    #     return p.statements

    @_('ID ASSIGN expr')
    def statement(self, p):
        # self.names[p.ID] = p.expr
        return AstNode("ASSIGN", p.ID, p.expr)
    
    # @_('ID LPAREN ARG')

    @_('expr SEMI')
    def statement(self, p):
        return p.expr
    
    # @_('IF LPAREN expr RPAREN { statements }')
    # def statement(self, p):
    #     return AstNode("IF", p.expr, p.statement)
    #
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
    
    @_('term GOE factor')
    def term(self, p):
        return AstNode("GOE", p.term, p.factor)

    @_('term SOE factor')
    def term(self, p):
        return AstNode("SOE", p.term, p.factor)

    @_('term SMALLER factor')
    def term(self, p):
        return AstNode("SMALLER", p.term, p.factor)

    @_('term GREATER factor')
    def term(self, p):
        return AstNode("GREATER", p.term, p.factor)

    # @_('{ statements }')
    # def statements(self, p):
    #     return p.statements

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

def main():
    lexer = MyLangLexer()
    parser = MyLangParser()
    text = open("./function.mylang").read()
    if text:
        tokens = lexer.tokenize(text)
        try:
            result = parser.parse(tokens)
            # print(str(parser._lrtable))
            print(result)
            # for statement in result:
            #     print(statement)
            # print(result)
            # print(parser.names)
        except NameError as e:
            print(f"Error: {e}")
    else:
        pass
if __name__ == "__main__":
    main()
