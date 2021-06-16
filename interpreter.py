from calc_excepts import InterpreterException, EnvironmentException
from nodes import *
from math_func import *

class Environment:
    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.variables = {}
        self.builtin_functions = {'sqrt': sqrt,
                                  'test': test_func,}
        self.user_functions = {}
        self.func_parameters = []

    def put(self, identifier, value):
        self.variables[identifier] = value

    def get(self, identifier):
        try:
            return self.variables[identifier]
        except KeyError:
            raise EnvironmentException(f"Environment: variable ({identifier}) does not exist")

    def call(self, func_name, parameters):
        if func_name in self.builtin_functions:
            return self.builtin_functions[func_name](*parameters)
        elif func_name in self.user_functions:
            return 99
        else:
            raise EnvironmentException("Environment: Unknown function")

    def create_func(self, func_name, args, expr_tree):
        pass


class Interpreter:
    def __init__(self):
        self.env = Environment(self)

    def check(self, node):
        type_ = type(node)
        # Binary operations
        if type_ is ArithmeticNode:
            func = ARITHMETIC[node.operation]
            return func(self.check(node.node_a), self.check(node.node_b))

        #Unary operations
        elif type_ is UnaryNode:
            func = UNARY[node.type]
            return func(self.check(node.child))

        #retrieve basic data
        elif type_ in (DataNode, StringNode):
            return node.value

        #call functions
        elif type_ is CallNode:
            args = [self.check(arg) for arg in node.args]
            return self.env.call(node.name, args)

        #map values
        elif type_ is FuncAssignNode:
            print(node)
            return 0
        elif type_ is AssignmentNode:
            #node.name is a VarNode which has a hashable field 'name', names need to be varied
            self.env.put(node.name.name, self.check(node.expr))
            return self.env.get(node.name.name)

        #retrieve mapped value
        elif type_ is VarNode:
            return self.env.get(node.name)

        else:
            raise InterpreterException(f'Interpreter: WTF is this? {type_}')

