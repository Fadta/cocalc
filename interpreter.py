from calc_excepts import CocalcException
from nodes import *

def add(n1, n2): return n1 + n2
def sub(n1, n2): return n1 - n2
def mul(n1, n2): return n1 * n2
def div(n1, n2): return n1 / n2

ARITHMETIC={'+': add, '-': sub, '*': mul, '/': div}

def neg(n): return -n
def nop(n): return n
UNARY={'-': neg, '+': nop}

class Interpreter:
    def check(self, node):
        type_ = type(node)
        if type_ is ArithmeticNode:
            func = ARITHMETIC[node.operation]
            return func(self.check(node.node_a), self.check(node.node_b))

        elif type_ is UnaryNode:
            func = UNARY[node.type]
            return func(self.check(node.child))

        elif type_ is DataNode:
            return node.value

        else:
            raise CocalcException(f'Interpreter: WTF is this? {type_}')

