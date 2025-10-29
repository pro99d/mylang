from lexer import MyLangLexer
from parser import MyLangInterpreter, MyLangParser, ml_function



@ml_function
def print_(*args, **kargs):
    print(*args, **kargs)


@ml_function
def type_(*args, **kargs):
    return type(*args, **kargs)

def main():
    lexer = MyLangLexer()
    parser = MyLangParser()
    interpreter = MyLangInterpreter()
    text = open("./simple.mylang").read()
    if text:
        tokens = lexer.tokenize(text)
        try:
            result = parser.parse(tokens)
            for statement in result:
                interpreter.interpret(statement)
        except NameError as e:
            print(f"Error: {e}")
    else:
        pass


if __name__ == "__main__":
    main()
