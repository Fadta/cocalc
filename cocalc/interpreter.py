from cocalc.calc_excepts import InterpreterException, EnvironmentException
from cocalc.nodes import *
import cocalc.math_func as mf
import sympy
import math


class Environment:
    """
    The Environment is a group of static variables,
    where the interpreter can put and retrieve values
    """

    def __init__(self, interpreter=None):
        """
        A interpreter may retrieve values of the Environment
        but it needs to associate itself with it first
        """
        self.interpreter = interpreter
        self.variables = {'ans': 0, 'e': math.e, 'pi': sympy.pi, 'inf': sympy.oo}
        self.builtin_functions = {'sqrt': sympy.sqrt,
                                  'log': sympy.log,
                                  'cos': sympy.cos,
                                  'sin': sympy.sin,
                                  'tan': sympy.tan,
                                  'sec': sympy.sec,
                                  'csc': sympy.csc,
                                  'cot': sympy.cot,
                                  'acos': sympy.acos,
                                  'asin': sympy.asin,
                                  'atan': sympy.atan,
                                  'asec': sympy.asec,
                                  'acsc': sympy.acsc,
                                  'acot': sympy.acot,
                                  'test': mf.test_func,
                                  'expand': sympy.expand,
                                  'factor': sympy.factor,
                                  'lim': mf.lim,
                                  'diff': sympy.diff,
                                  'int': sympy.integrate,
                                  'latex': sympy.latex,
                                  }
        self.user_functions = {}
        self.func_parameters = []

    def assign_interpreter(self, interpreter):
        """
        Change current associated interpreter
        """
        self.interpreter = interpreter

    def put(self, identifier, value):
        """
        Store a variable identifier with its value
        inside the environment
        """
        self.variables[identifier] = value

    def get(self, identifier, scope):
        """
        Retrieve a stored variable identifier
        of the corresponding scope:
            0- global
            1- function argument

        raises EnvironmentException if:
            -scope is not defined (see up)
            -identifier does not exist
        """
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
        """
        put the function parameters in a
        'stack-like' data structure so the
        function call may use them
        """
        for param in params:
            self.func_parameters.append(param)

    def call(self, func_name, parameters):
        """
        search func_name in builtin_functions:
            if it exists then uncompress the
            raw data of parameters

            Exceptions of builtin_functions are
            treated and printed so program doesn't crash

        elif search func_name in user_functions:
            if it exists then retrieve the expr_tree
                load_parameters

                walk with the associated interpreter
                the expr_tree

        raises EnvironmentException if:
            there are more or less parameters than required
            or
            func_name is not in builtin_functions nor user_functions

        """
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
        """
        store an expression tree associated with the func_name
        args contain a tuple (funcVarId, expr_treeVarName)
        """
        arg_len = len(args)
        val = (arg_len, expr_tree)
        self.user_functions[func_name] = val


class Interpreter:
    """
    The interpreter walks the execution tree
    and executes each node
    """
    def __init__(self, env: Environment):
        self.env = env
        self.env.assign_interpreter(self)

    def check(self, node):
        """
        start to walk starting from this node
        evaluate node (by type) and then check() childs
        """
        type_ = type(node)
        # Binary operations
        if type_ is ArithmeticNode:
            func = mf.ARITHMETIC[node.operation]
            return func(self.check(node.node_a), self.check(node.node_b))

        # Unary operations
        elif type_ is UnaryNode:
            func = mf.UNARY[node.type]
            return func(self.check(node.child))

        # retrieve basic data
        elif type_ in (DataNode, StringNode):
            return node.value

        # call functions
        elif type_ is CallNode:
            args = [self.check(arg.value) for arg in node.args]
            return self.env.call(node.name, args)

        # map values
        elif type_ is FuncAssignNode:
            self.env.create_func(node.func_expr.name, node.func_expr.args, node.expr_tree)
            return 1
        elif type_ is AssignmentNode:
            # node.name is a VarNode which has a hashable field 'name', names need to be varied
            self.env.put(node.name.name, self.check(node.expr))
            return self.env.get(node.name.name, node.name.scope)

        # retrieve mapped value
        elif type_ is VarNode:
            return self.env.get(node.name, node.scope)

        else:
            raise InterpreterException(f'Interpreter: WTF is this? {type_}')
