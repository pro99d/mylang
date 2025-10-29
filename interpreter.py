from exceptions import RED, CLEAR
from namespace import ml_globals

class MyLangInterpreter:
    def __init__(self):
        pass
    def interpret(self, data):
        op = data.op 
        left = data.l 
        right = data.r
        i = self.interpret
        match op:
            case "NUMBER":
                return left
            case "ASSIGN":
                ml_globals[left] = i(right)
                return i(right)
            case "READ":
                if left in ml_globals:
                    return ml_globals[left]
                else:
                    raise NameError(f"{RED}Undefined name {CLEAR}{left}")
            case "ADD":
                return i(left)+i(right)
            case "SUB":
                return i(left)-i(right)
            case "MUL":
                return i(left)*i(right)
            case "DIV":
                return i(left)/i(right)
            case "CALL":
                right = list(map(i, right))
                return left(*right)
            case _:
                print(f"{RED}Unknown operation {CLEAR}{op}")
                return
