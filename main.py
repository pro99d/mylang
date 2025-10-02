globals = {}
SPEC_CHR = [" ", "=", "\n", ";", "==", ">", "<", "<=", ">=", "+", "-", "/", "*"]

class variable:
    def __init__(self, name, _type, value):
        self.name = name
        self.type = _type
        self.value = value

def is_string(s: str):
    symb = s[0]
    if s[0] != '"' and s[-1] != '"':
        return False
    return s.count('"')==2
     

def parse_line(line: str):
    cur_string = ''
    result = []

    for i in line:
        if i not in SPEC_CHR:
            cur_string+=i 
            continue
        elif i == " ":
            result.append(cur_string)
            cur_string = ""
            continue
        elif i == "=":
            result.append(cur_string)
            cur_string = ""
            result.append('=')
            continue
    result.append(cur_string)
    for d, i in enumerate(result):
        if not i:
            result.remove(i)
        if i.isnumeric():
            result[d] = int(i)
    print(result)
def main():
    f = open("./example.mylang", 'r').readlines()
    for l in f:
        parse_line(l)


if __name__ == "__main__":
    main()
