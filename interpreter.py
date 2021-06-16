from calc_excepts import CocalcException
from nodes import *
from math_func import *

class Environment:
    def __init__(self):
        self.variables = {}

    def put(self, identifier, value):
        self.variables[identifier] = value

    def get(self, identifier):
        return self.variables[identifier]

class Interpreter:
    def __init__(self):
        self.env = Environment()

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

        elif type_ is AssignmentNode:
            #node.name is a VarNode which has a hashable field 'name', names need to be varied
            self.env.put(node.name.name, self.check(node.expr))
            return self.env.get(node.name.name)

        elif type_ is VarNode:
            return self.env.get(node.name)

        else:
            raise CocalcException(f'Interpreter: WTF is this? {type_}')

