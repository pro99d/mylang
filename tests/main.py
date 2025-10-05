import re
from exceptions import RED, CLEAR
globals = {}
SPEC_CHR = [" ", "=", "\n", ";", "==", ">",
            "<", "<=", ">=", "+", "-", "/", "*"]
# паттерны


class Patterns:
    set_pattern = r'^[^=]+=[^=]+$'
    float_pattern = r'^[\d^.]?.[\d^.]?$'
    call_pattern = r'^[]+([]+)$'


class Variable:
    def __init__(self, name, _type, value):
        self.name = name
        self.type = _type
        self.value = value

    def __repr__(self) -> str:
        return str(self.value)

    # арифметические операции
    def __add__(self, other):
        if type(other) is self:
            return self.value+other.value
        return self.value+other

    def __radd__(self, other):
        if type(other) is self:
            return self.value+other.value
        return self.value+other

    def __div__(self, other):
        if type(other) is self:
            return self.value/other.value
        return self.value/other

    def __rdiv__(self, other):
        if type(other) is self:
            return other.value/self.value
        return other/self.value

    def __mul__(self, other):
        if type(other) is self:
            return self.value*other.value
        return self.value*other

    def __rmul__(self, other):
        if type(other) is self:
            return self.value*other.value
        return self.value*other


class Function:
    def __init__(self, values):
        self.values = values

    def __call__(self, *args, **kargs):
        pass


variables = {}  # имя: Variable
"""
 
"""


class Keyword:
    pass


class Expression:
    # TODO реализовать вложенные выражения
    def __init__(self, value, expr_subtype: str, expr_type: str = "bin") -> None:
        self.expr = value
        self.expr_type = expr_type
        self.expr_subtype = expr_subtype

    def find_result(self):
        match self.expr_type:
            case "bin":
                match self.expr_subtype:
                    case "set":
                        e = list(map(str, self.expr))
                        set_var = e[0]
                        set_value = e[2]

                        if is_string(set_value):
                            set_type = str
                            set_value = set_value[1:-1]
                        elif set_value.isnumeric and '.' not in set_value:
                            set_type = int
                        elif re.fullmatch(Patterns.float_pattern, set_value):
                            set_type = float
                        else:
                            set_type = type(set_value)
                        variables[set_var] = Variable(
                            set_var, set_type, set_type(set_value))
                    case "add":
                        pass  # TODO result[::-1] ?
            case _:
                raise Exception(
                    f"Нереализованный тип выражения: {self.expr_type}")

    def __repr__(self) -> str:
        return str(self.expr)  # [1:-1]


def is_string(s: str):
    if s[0] != '"' and s[-1] != '"':
        return False
    return s.count('"') == 2


def delete_empty(wtp: list) -> list:
    for d, i in enumerate(wtp):
        if i in (" ", ""):
            wtp.remove(i)
    return wtp


def devide_by_spec(line: str):
    cur_string = ''
    result = []
    for i in line:
        if i in SPEC_CHR:
            if cur_string:
                result.append(cur_string)
            cur_string = ""
            result.append(i)
            continue
        cur_string += i
    if cur_string:
        result.append(cur_string)
    result = delete_empty(result)
    for d, i in enumerate(result):
        if i.isnumeric():
            result[d] = int(i)
    while result.count("\n"):
        result.remove('\n')
    return result


def devide_to_lines(r):
    result = [""]
    r = iter(r)
    prev = None
    while True:
        try:
            i = next(r)
            if i != ";":
                result[-1] += str(i)
            else:
                result.append("")
            prev = i
        except StopIteration:
            break
    result = delete_empty(result)
    return result


def parse_line(line: str):
    result = devide_by_spec(line)
    result = iter(result)
    f_res = []
    prev = None
    while True:
        try:
            i = next(result)
            
            match i:
                case "=":
                    if not prev:
                        log = ""
                        log+=i
                        while i not in (';', '\n'):
                            try:
                                i = next(result)
                                log+=i
                            except StopIteration:
                                break
                        raise Exception(f"{RED}Синтаксическая ошибка: {CLEAR}{log}")
                    f_res.append(Expression([prev, i, next(result)], "set"))

            prev = i
        except StopIteration:
            break
    # result = devide_to_lines(result)
    # for d, i in enumerate(result):
    #     if re.fullmatch(Patterns.set_pattern, i):
    #         result[d] = Expression(i, "set")
    #     else:
    #         result[d] = Expression(i, "undefined")

    return f_res


def execute_expressions(expressions: list[Expression]) -> None:
    for i in expressions:
        i.find_result()


def main():
    f = "".join(open("./example.mylang", 'r').readlines())
    parsed = parse_line(f)
    execute_expressions(parsed)
    print(parsed)
    print(variables)


if __name__ == "__main__":
    main()
