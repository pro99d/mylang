# cython: overflowchech=False
cimport cython
import numpy as np
from exceptions import RED, CLEAR 
from ml_namespace import ml_globals
# cython: c_long_type=np.int64
    
class MyLangInterpreter:
    def __init__(self):
        self.conditions = {"GOE": ">=", "SOE": "<=",
                           "SMALLER": "<", "GREATER": ">"}
    @cython.cdivision(True)
    def interpret(self, data):
        global ml_globals
        # cython.overflowchech(False)
        cdef long long int l
        # cdef Variable r
        cdef str d
        op = data.op
        left = data.l
        right = data.r
        other = data.other
        i = self.interpret
        if op == "BREAK":
            return "BREAK"
        elif op == "CONTINUE":
            return "CONTINUE"
        elif op == "NOP":
            return None
        elif op == "NUMBER":
            l = left
            return l
        elif op == "STRING":
            return left
        elif op == "ASSIGN":
            r = i(right)
            ml_globals[left] = r
            # print(ml_globals)
            return r
        elif op == "READ":
            # print(ml_globals)
            if left in ml_globals:
                return ml_globals[left]
            else:
                raise NameError(f"{RED}Undefined name {CLEAR}{left}{RED} at {CLEAR}{other[0]}")
        elif op == "ADD":
            l = i(left)
            r = i(right)
            return l + r
        elif op == "SUB":
            l = i(left)
            r = i(right)
            return l-r
        elif op == "MUL":
            l = i(left)
            r = i(right)
            return l*r
        elif op == "DIV":
            l = i(left)
            r = i(right)
            return l/r
        elif op == "CALL":
            right = list(map(i, right))
            # kargs = other[0]
            # kargs = dict(zip(kargs.keys(), list(map(i, kargs.values()))))
            return left(*right)
        elif op == "cond":
            d = self.conditions[other[0]]
            l = i(left)
            r = i(right)
            if d == ">":
                return r > r 
            elif d == "<":
                return l < r
            elif d == ">=":
                return l >= r
            elif d == "<=":
                return l <= r
            elif d == "not":
                return not l
            elif d == "and":
                return l and r
            elif d == "or":
                return l or r
            else:
                print(f"{RED} Unknown operator: {CLEAR}{d}")
                exit()
        elif op == "IF":
            l = i(left)
            if l:
                for statement in right:
                    i(statement)
            else:
                for statement in other:
                    i(statement)
            return
        elif op == "ELSE":
            for statement in left.l:
                i(statement)
        elif op == "WHILE":
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
        else:
            print(f"{RED}Unknown operation {CLEAR}{op}")
            return
