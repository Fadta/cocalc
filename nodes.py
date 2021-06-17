from dataclasses import dataclass
import tokens

@dataclass
class DataNode:
    """
    Stores data that can be manipulated
    """
    value: any

    def __repr__(self):
        return f"{self.value}"

@dataclass
class StringNode:
    value: str

    def __repr__(self):
        return value

@dataclass
class ArithmeticNode:
    operation: tokens.Values
    node_a: any
    node_b: any

    def __repr__(self):
        return f"({self.node_a} {self.operation} {self.node_b})"

@dataclass
class VarNode:
    """
    name: name of the variable
    scope: the scope in which the variable is used
        0: global
        1: function parameter
    """
    name: any
    scope: int

    def __repr(self):
        return f"{self.name}[{self.scope}]"

@dataclass
class FuncParameter:
    identifier: str
    value: any

    def __repr__(self):
        return f"({self.identifier}:{self.value})"

@dataclass
class CallNode:
    name: str
    args: FuncParameter

    def __repr__(self):
        return f"{self.name}{self.args}"

@dataclass
class UnaryNode:
    type: any
    child: any

    def __repr__(self):
        return f"({self.type}{self.child})"

@dataclass
class FuncVarNode:
    name: str

@dataclass
class FuncAssignNode:
    func_expr: CallNode
    expr_tree: any

    def walk_and_replace(self, node, search_for, real_name):
        node_type = type(node)
        if node_type is ArithmeticNode:
            self.walk_and_replace(node.node_a, search_for, real_name)
            self.walk_and_replace(node.node_b, search_for, real_name)
        elif node_type is UnaryNode:
            self.walk_and_replace(node.child, search_for, real_name)
        elif node_type is VarNode:
            if node in search_for:
                node.name = real_name[node.name]
                node.scope = 1
        return

    def link_variables(self):
        name_dict = {}
        search_for = []
        #param.value in func_expr should be a string containing the name of the nomenclated
        for param in self.func_expr.args:
            search_for.append(param.value)
            name_dict[param.value.name] = param.identifier

        self.walk_and_replace(self.expr_tree, search_for, name_dict)

    def __repr__(self):
        return f"({self.func_expr}: {self.expr_tree})"

@dataclass
class AssignmentNode:
    name: VarNode
    expr: any

    def __repr__(self):
        return f"{self.name} = {self.expr}"
