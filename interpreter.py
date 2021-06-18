from calc_excepts import InterpreterException, EnvironmentException
from nodes import *
from math_func import *
import sympy
import math

class Environment:
    def __init__(self, interpreter = None):
        self.interpreter = interpreter
        self.variables = {'ans': 0, 'e': math.e, 'pi': math.pi}
        self.builtin_functions = {'sqrt': sqrt,
                                  'test': test_func,
                                  'expand': sympy.expand,
                                  'factor': sympy.factor,}
        self.user_functions = {}
        self.func_parameters = []

    def put(self, identifier, value):
        self.variables[identifier] = value

    def get(self, identifier, scope):
        try:
            if scope == 0:
                return self.variables[identifier]
            elif scope == 1:
                return self.func_parameters[int(identifier)]
            else:
                raise EnvironmentException(f"Environment: variable scope ({self.scope}) is not defined")
        except KeyError:
            raise EnvironmentException(f"Environment: variable ({identifier}) does not exist")

    def load_parameters(self, params: list):
        for param in params:
            self.func_parameters.append(param)

    def call(self, func_name, parameters):
        if func_name in self.builtin_functions:
            try:
                return self.builtin_functions[func_name](*parameters)
            except Exception as e:
                raise EnvironmentException(f'Environment: function {func_name}{tuple(parameters)} raised:\n\t {e}')

        elif func_name in self.user_functions:
            param_size = self.user_functions[func_name][0]
            if len(parameters) != param_size:
                raise EnvironmentException(f'Environment: function {func_name} expected {param_size} arguments but {len(parameters)} were given ')
            expr_tree = self.user_functions[func_name][1]
            self.load_parameters(parameters)
            result = self.interpreter.check(expr_tree)
            self.func_parameters = []
            return result

        else:
            raise EnvironmentException("Environment: Unknown function")

    def create_func(self, func_name, args, expr_tree):
        arg_len = len(args)
        val = (arg_len, expr_tree)
        self.user_functions[func_name] = val


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
            args = [self.check(arg.value) for arg in node.args]
            return self.env.call(node.name, args)

        #map values
        elif type_ is FuncAssignNode:
            self.env.create_func(node.func_expr.name, node.func_expr.args, node.expr_tree)
            return 1
        elif type_ is AssignmentNode:
            #node.name is a VarNode which has a hashable field 'name', names need to be varied
            self.env.put(node.name.name, self.check(node.expr))
            return self.env.get(node.name.name, node.name.scope)

        #retrieve mapped value
        elif type_ is VarNode:
            return self.env.get(node.name, node.scope)

        else:
            raise InterpreterException(f'Interpreter: WTF is this? {type_}')

