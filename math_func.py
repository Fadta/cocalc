import math

def add(n1, n2): return n1 + n2
def sub(n1, n2): return n1 - n2
def mul(n1, n2): return n1 * n2
def div(n1, n2): return n1 / n2
ARITHMETIC={'+': add, '-': sub, '*': mul, '/': div, '^': pow}

def neg(n): return -n
def nop(n): return n
UNARY = {'-': neg, '+': nop}

def sqrt(n): return math.sqrt(n)
def test_func(*args):
    string = ''
    for arg in args:
        string += str(arg)
    return float(string)
