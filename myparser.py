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
        pass

    def can_process(self, data: tuple[str]) -> bool:
        started = []
        for x in self.rlist:
            # print(x, data)
            if x == data:
                started.append(x)
        return len(started) == 1
    


def main():
    lexer = MyLangLexer()
    parser = Parser()
    string = "4"
    lexed = list(lexer.tokenize(string))
    print(parser.parse(lexed))


if __name__ == "__main__":
    main()
