from exceptions import RED, CLEAR
from namespace import ml_globals


class MyLangInterpreter:
    def __init__(self):
        self.conditions = {"GOE": ">=", "SOE": "<=",
                           "SMALLER": "<", "GREATER": ">"}

    def interpret(self, data):
        global ml_globals
        op = data.op
        left = data.l
        right = data.r
        other = data.other
        i = self.interpret
        match op:
            case "BREAK":
                return "BREAK"
            case "CONTINUE":
                return "CONTINUE"
            case "NOP":
                return None
            case "NUMBER":
                return left
            case "STRING":
                return left
            case "ASSIGN":
                ml_globals[left] = i(right)
                # print(ml_globals)
                return i(right)
            case "READ":
                # print(ml_globals)
                if left in ml_globals:
                    return ml_globals[left]
                else:
                    raise NameError(f"{RED}Undefined name {CLEAR}{left}{RED} at {CLEAR}{other[0]}")
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
            case "cond":
                d = self.conditions[other[0]]
                left = i(left)
                right = i(right)
                match d:
                    case ">":
                        return left > right
                    case "<":
                        return left < right
                    case ">=":
                        return left >= right
                    case "<=":
                        return left <= right
                    case "not":
                        return not left
                    case "and":
                        return left and right
                    case "or":
                        return left or right
                    case _:
                        print(f"{RED} Unknown operator: {CLEAR}{d}")
                        exit()
            case "IF":
                if i(left):
                    for statement in right:
                        i(statement)
                else:
                    for statement in other:
                        i(statement)
                return
            case "ELSE":
                for statement in left.l:
                    i(statement)

            case "WHILE":
                while i(left):
                    for statement in right:
                        r = i(statement)
                        if r == "BREAK":
                            break
                        elif r == "CONTINUE":
                            continue
                # else:
                #     for statement in other:
                #         i(statement)

            case _:
                print(f"{RED}Unknown operation {CLEAR}{op}")
                return
