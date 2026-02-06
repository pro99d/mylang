from exceptions import RED, CLEAR
import ml_namespace as ns


class MyLangInterpreter:
    def __init__(self):
        self.conditions = {"GOE": ">=", "SOE": "<=",
                           "SMALLER": "<", "GREATER": ">",
                           "not":"not", "and":"and", "or":"or"}

    def interpret(self, data):
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
            case "LIST":
                return list(map(i, left))
            case "STRING":
                return left
            case "ASSIGN":
                ns.write_value(left, i(right))
                # print(ml_globals)
                return i(right)
            case "READ":
                # print(ml_globals)
                return ns.get_value(left)
            case "ADD":
                return i(left)+ i(right)
            case "SUB":
                return i(left)-i(right)
            case "MUL":
                return i(left)*i(right)
            case "DIV":
                return i(left)/i(right)
            case "FUNC":
                ns.write_value(left, right)
            case "RETURN":
                return i(left)
            case "CALL":
                right = list(map(i, right))
                name = left
                left = ns.get_value(left)
                if left["type"] == "py":
                    # kargs = other[0]
                    # kargs = dict(zip(kargs.keys(), list(map(i, kargs.values()))))
                    return left["call"](*right)
                elif left['type'] == "ml":
                    ns.add_namespace()
                    if len(right) != len(left["args"]):
                        raise TypeError(f"{name}{RED} takes {len(left['args'])} positional arguments, but {len(right)} given")
                    for d, id in enumerate(left["args"]):
                        ns.write_value(id.l, right[d])
                    for statement in left['call']:
                        ret = i(statement)
                        if ret != None:
                            return ret

            case "cond":
                d = other[0].value
                left = i(left)
                if right:
                    right = i(right)
                match d:
                    case ">":
                        return left > right
                    case "<":
                        return left < right
                    case "==":
                        return left == right
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
                        p =  i(statement)
                        if statement.op == "RETURN":
                            return p
                else:
                    for statement in other:
                        p = i(statement)
                        if statement.op == "RETURN":
                            return p
                return
            # case "ELSE":
            #     for statement in left.l:
            #         i(statement)
            case "EXEC":
                return eval(left)

            case "WHILE":
                while i(left):
                    for statement in right:
                        r = i(statement)
                        if r == "BREAK":
                            return 
                        elif r == "CONTINUE":
                            break
                # else:
                #     for statement in other:
                #         i(statement)

            case _:
                print(f"{RED}Unknown operation {CLEAR}{op}")
                return
