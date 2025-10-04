RED = "\033[31m"
CLEAR = "\033[0m"
BOLD = "\033[1m"

class MylangException(Exception):
    def __init__(self, message: str= "", *args: object) -> None:
        self.message = f"{RED}{message}{CLEAR}"
        # self.message  =f"{BOLD}{RED}{self.__class__.__name__}{CLEAR}: {self.message}"
        super().__init__(self.message, *args)

class NotVariableSetExpression(MylangException):
    def __init__(self, *args: object) -> None:
        super().__init__("Попытка присваивания не переменной!", *args)

if __name__ == "__main__":
    raise NotVariableSetExpression
