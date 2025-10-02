import re
globals = {}
SPEC_CHR = [" ", "=", "\n", ";", "==", ">",
            "<", "<=", ">=", "+", "-", "/", "*"]
# паттерны
set_pattern = r'^[^=]+=[^=]+$'


class Variable:
    def __init__(self, name, _type, value):
        self.name = name
        self.type = _type
        self.value = value
    def __repr__(self) -> str:
        return str(self.value)

variables = {}  # имя: Variable


class Expression:
    # TODO реализовать вложенные выражения
    def __init__(self, value: str, expr_type: str) -> None:
        self.expr = value
        self.expr_type = expr_type

    def find_result(self):
        match self.expr_type:
            case "set":
                e = self.expr.split("=")
                set_var = e[0]
                set_value = e[1]
                if is_string(set_value): #FIXME тип и значение c - строка
                    set_type = str
                    set_value = set_value[1:-1]
                elif set_value.isnumeric:
                    set_type = int
                else:
                    set_type = type(set_value)

                variables[set_var] = Variable(set_var, set_type, set_value)
            case _:
                raise Exception(
                    f"Unimplemented expression type: {self.expr_type}")

    def __repr__(self) -> str:
        return self.expr[1:-1]


def is_string(s: str):
    if s[0] != '"' and s[-1] != '"':
        return False
    return s.count('"') == 2


def delete_empty(wtp: list) -> list:
    for d, i in enumerate(wtp):
        if i in (" ", ""):
            wtp.remove(i)
    return wtp


def devide_to_lines(r):
    result = [""]
    for i in r:
        if i != ";":
            result[-1] += str(i)
        else:
            result.append("")
    result = delete_empty(result)
    return result


def parse_line(line: str):
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

    result = devide_to_lines(result)

    for d, i in enumerate(result):
        if re.fullmatch(set_pattern, i):
            result[d] = Expression(i, "set")
        else:
            result[d] = Expression(i, "undefined")

    
    return result

def execute_expressions(expressions: list[Expression]) -> None:
    for i in expressions:
        i.find_result()

def main():
    f = "".join(open("./example.mylang", 'r').readlines())
    parsed = parse_line(f)
    execute_expressions(parsed)
    print(parsed)
    print(variables)
    print(type(variables['c'].value))


if __name__ == "__main__":
    main()
