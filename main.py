from lexer import MyLangLexer
from parser import MyLangInterpreter, MyLangParser, ml_function
import sys


@ml_function
def print_(*args, **kargs):
    sys.stdout.write(str(*args, **kargs)+"\n")


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
            i = 0
            labels = {}
            while True:
                try:
                    statement = result[i]
                except IndexError:
                    break
                interpreter.interpret(statement)
                i+=1
        except NameError as e:
            print(f"Error: {e}")
    else:
        pass


if __name__ == "__main__":
    main()
