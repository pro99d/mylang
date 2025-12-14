from ml_lexer import MyLangLexer
import copy 

rules = {}
# TODO

class AstNode:
    def __init__(self, op, left, right=None, other=[]):
        self.op = op
        self.l = left
        self.r = right
        self.other = other

    def __repr__(self):
        return f"({self.op}, {self.l}, {self.r}, {self.other})"


def rule(inp: str):
    inp_formated = inp.split(" ")
    inp_formated = tuple(inp_formated)

    def decorator(func):
        rules[inp_formated] = {"type": func.__name__, "func": func}

        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            return result
        return wrapper
    return decorator


class Token:
    def __init__(self, type: str, value, lineno: int, index: int, end: int) -> None:
        self.type: str = type
        self.value = value
        self.lineno = lineno
        self.index = index
        self.end = end
    def __repr__(self) -> str:
        return f"Token(type= {self.type}, value= {self.value}, lineno= {self.lineno}, index= {self.index}, end= {self.end})"
        


class Rule:
    def __init__(self) -> None:
        pass


class Parser:
    def __init__(self) -> None:
        global rules
        self.rlist: list = list(rules.keys())
        self.maxlen = max(map(lambda x: len(x), self.rlist))

    def gen_names(self, names: list[str]) -> list[str]:
        result = []
        amount = {}
        for name in names:
            if name in amount.keys():
                amount[name] += 1
            else:
                amount[name] = 1
            n = f"{name}{amount[name]}"
            if amount[name] > 1 and n not in result:
                result.append(n)
            else:
                result.append(name)
        return result

    def parse(self, tokens: list):
        toplevel = "factor" # TODO:
        repeat = 0
        prevtok = []
        while tokens:
            parsed = False
            for st in range(0, self.maxlen):
                for i in range(self.maxlen, 0, -1):
                    cur = tokens[st:i]
                    names = list(map(lambda x: x.type, cur))
                    if self.can_process(tuple(names)):
                        print(f"can process {cur}")
                        attrs = self.gen_names(names)
                        p = Rule()
                        ln = cur[0].lineno
                        ind = cur[0].index
                        end = cur[-1].end
                        for i, d in enumerate(attrs):
                            p.__setattr__(d, cur[i].value)
                        value = rules[tuple(names)]["func"](self, p)
                        type_ = rules[tuple(names)]["type"]
                        for _ in range(i+1):
                            tokens.pop(0)
                        tokens.insert(0, Token(
                            type= type_,
                            value= value,
                            lineno= ln,
                            index= ind,
                            end= end
                        ))
                        parsed = True
                        print(tokens)
                        break
            if tokens in prevtok:
                return tokens
            else:
                prevtok.append(tokens)

    def can_process(self, data: tuple[str]) -> bool:
        started = []
        for x in self.rlist:
            # print(x, data)
            if x == data:
                started.append(x)
        return len(started) == 1
    

    @rule('term')
    def expr(self, p):
        return p.term

    @rule('term COMPARE factor')
    def cond(self, p):
        return AstNode("cond", p.term, p.factor, other=["COMPARE"])

    @rule('term TIMES factor')
    def term(self, p):
        return AstNode("TIMES", p.term, p.factor)

    @rule('term DIVIDE factor')
    def term(self, p):
        return AstNode("DIVIDE", p.term, p.factor)

    @rule('factor')
    def term(self, p):
        return p.factor

    @rule('NUMBER')
    def factor(self, p):
        return AstNode("NUMBER", p.NUMBER)

    @rule("factor PLUS NUMBER")
    def factor(self, p):
        return AstNode("PLUS",p.factor, p.NUMBER)

    # @rule("statements")
    # def program(self, p):
    #     return p.statements
    #
    # @rule("statements statement")
    # def statements(self, p):
    #     return p.statements + [p.statement]
    #
    # @rule('IF LPAREN cond RPAREN LBRACE statements RBRACE else_')
    # def statement(self, p):
    #     return AstNode("IF", p.cond, p.statements, other=[AstNode("ELSE", p.else_)])


def main():
    lexer = MyLangLexer()
    parser = Parser()
    string = "4==2"
    lexed = list(lexer.tokenize(string))
    print(parser.parse(lexed))


if __name__ == "__main__":
    main()
