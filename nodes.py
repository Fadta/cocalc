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
class AddNode:
    node_a: any
    node_b: any

    def __repr__(self):
        return f"({self.node_a} + {self.node_b})"

@dataclass
class SubNode:
    node_a: any
    node_b: any

    def __repr__(self):
        return f"({self.node_a} - {self.node_b})"

@dataclass
class MulNode:
    node_a: any
    node_b: any

    def __repr__(self):
        return f"({self.node_a} * {self.node_b})"

@dataclass
class DivNode:
    node_a: any
    node_b: any

    def __repr__(self):
        return f"({self.node_a} / {self.node_b})"

@dataclass
class ExpNode:
    node_a: any
    node_b: any

    def __repr__(self):
        return f"({self.node_a} ^ {self.node_b})"

@dataclass
class ArithmeticNode:
    operation: tokens.Values
    node_a: any
    node_b: any

    def __repr__(self):
        return f"({self.node_a} {self.operation} {self.node_b})"

@dataclass
class NegNode:
    node: any

    def __repr__(self):
        return f"(-{self.node})"

@dataclass
class SumNode:
    node:any

    def __repr__(self):
        return f"(+{self.node})"

@dataclass
class VarNode:
    name: any

    def __repr(self):
        return f"{self.name}"

@dataclass
class CallNode:
    function_pointer: any
    args: list

    def __repr__(self):
        return f"{self.function_pointer}{self.args}"

@dataclass
class UnaryNode:
    type: any
    child: any

    def __repr__(self):
        return f"({self.type}{self.child})"

@dataclass
class AssignmentNode:
    name: VarNode
    expr: any

    def __repr__(self):
        return f"{self.name} = {self.value}"
