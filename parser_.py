from tokens import Values, TokenType
from calc_excepts import CocalcException
from nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = iter(tokens)
        self.advance()

    def advance(self):
        try:
            self.current_token = next(self.tokens)
        except StopIteration:
            self.current_token = None

    def parse(self):
        if self.current_token == None:
            return None

        result = self.expr()

        if self.current_token != None:
            raise CocalcException("Parser: Excess tokens, parser commited sudoku")

        return result

    def expr(self):
        result = self.term()

        while self.current_token != None and (self.current_token.type == TokenType.ARITH_OPERATION) and (self.current_token.value in (Values.AR_ADD, Values.AR_SUB)):
            if self.current_token.value == Values.AR_ADD:
                self.advance()
                result = ArithmeticNode('+', result, self.term())
            else:
                self.advance()
                result = ArithmeticNode('-', result, self.term())

        return result

    def term(self):
        result = self.factor()

        while self.current_token != None and (self.current_token.type == TokenType.ARITH_OPERATION) and (self.current_token.value in (Values.AR_MUL, Values.AR_DIV)):
            if self.current_token.value == Values.AR_MUL:
                self.advance()
                result = ArithmeticNode('*', result, self.factor())
            else:
                self.advance()
                result = ArithmeticNode('/', result, self.factor())

        return result

    def factor(self):
        token = self.current_token

        if token.type == TokenType.PAREN and token.value == Values.PAREN_OPEN:
            self.advance()
            result = self.expr()

            if self.current_token.type != TokenType.PAREN or self.current_token.value != Values.PAREN_CLOSE:
                raise CocalcException("Parser: You didn't close the parenthesis")
            self.advance()
            return result

        elif (token.type == TokenType.INT) or (token.type == TokenType.FLOAT):
            self.advance()
            return DataNode(token.value)

        elif (token.type == TokenType.ARITH_OPERATION) and (token.value == Values.AR_SUB):
            self.advance()
            return UnaryNode('-', self.factor())

        elif (token.type == TokenType.ARITH_OPERATION) and (token.value == Values.AR_ADD):
            self.advance()
            return UnaryNode('+', self.factor())

        raise CocalcException("Parser: You commited an ucky wucky uwu. Check your syntax king")

