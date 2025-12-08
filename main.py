from ml_lexer import MyLangLexer
from ml_parser import MyLangParser, ml_function
import sys
USE_CYTHON = "--cython" in sys.argv
if USE_CYTHON:
    from ml_interpreter_cython import MyLangInterpreter
else:
    from ml_interpreter import MyLangInterpreter

@ml_function
def print_(*args, **kargs):
    print(*list(map(str, args)), **kargs)

@ml_function
def stdout_(*args):
    sys.stdout.write(*list(map(str, args)))

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
        # try:
        result = parser.parse(tokens)
        for statement in result:
            interpreter.interpret(statement)
        # except NameError as e:
            # print(f"Error: {e}")
    else:
        pass


if __name__ == "__main__":
    main()
