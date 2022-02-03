from enum import Enum, auto
from dataclasses import dataclass


class Values(Enum):
    # Arithmetic
    AR_DIV = auto()  # Division
    AR_MUL = auto()  # Multiplication
    AR_ADD = auto()  # Addition
    AR_SUB = auto()  # Substraction
    AR_EXP = auto()  # Exponentiation
    # Parenthesis
    PAREN_OPEN = auto()
    PAREN_CLOSE = auto()


class TokenType(Enum):
    INT = auto()
    FLOAT = auto()
    SYMBOL = auto()
    CHAR = auto()
    STRING = auto()
    CALL = auto()
    VAR = auto()
    ASSIGNMENT = auto()
    PAREN = auto()
    ARITH_OPERATION = auto()


@dataclass  # dataclass decorator makes a struct-like DS
class Token:
    """
    Token is a lexical unit of a line.
    """
    type: TokenType
    value: any

    def __repr__(self):
        return f"{self.type}" + (f": {self.value}" if self.value != None else "")
