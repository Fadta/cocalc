from calc_excepts import MathError
import math as m
import sympy as sp

def add(n1, n2): return n1 + n2
def sub(n1, n2): return n1 - n2
def mul(n1, n2): return n1 * n2
def div(n1, n2):
    if n2 == 0: raise MathError("God: I found that you tried to divide by zero, you can't, sorry")
    return n1 / n2
ARITHMETIC={'+': add, '-': sub, '*': mul, '/': div, '^': pow}

def neg(n): return -n
def nop(n): return n
UNARY = {'-': neg, '+': nop}

def sqrt(n): return m.sqrt(n)
def cos(n):
    if isinstance(n, sp.Expr):
        return sp.cos(n)
    elif type(n) in (int, float):
        return m.cos(n)
    else:
        raise MathError(f'Invalid literal type for {n}')

def lim(symbol, z0, expr): return sp.limit(expr, symbol, z0)

def test_func(*args):
    string = ''
    for arg in args:
        string += str(arg)
    return int(string)

