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
    name: any

    def __repr(self):
        return f"{self.name}"

@dataclass
class CallNode:
    name: str
    args: any

    def __repr__(self):
        return f"{self.name}{self.args}"

@dataclass
class UnaryNode:
    type: any
    child: any

    def __repr__(self):
        return f"({self.type}{self.child})"

@dataclass
class FuncAssignNode:
    func_expr: CallNode
    expr_tree: any

    def __repr__(self):
        return f"({self.func_expr}: {self.expr_tree})"

@dataclass
class FuncParameter:
    identifier: str
    value: any

    def __repr__(self):
        return f"[{self.identifier}:{self.value}]"

@dataclass
class AssignmentNode:
    name: VarNode
    expr: any

    def __repr__(self):
        return f"{self.name} = {self.expr}"
