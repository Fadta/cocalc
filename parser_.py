import sympy
from tokens import Values, TokenType
from calc_excepts import CocalcException
from nodes import *

class Parser:
    """
    The parser reads the tokens and prepares
    an execution tree for the interpreter

    This parser analyzes tokens in this priority lower -> higher:
    expressions (like addition and substraction)
    terms (terms separated by addition and substraction)
    factors (irreducible term)
    """
    def __init__(self, tokens):
        self.tokens = iter(tokens)
        self.advance()

    def advance(self):
        try:
            self.current_token = next(self.tokens)
        except StopIteration:
            self.current_token = None

    def parse(self):
        """
        Starts the parsing, returns an execution tree
        """
        if self.current_token == None:
            return None

        result = self.expr()

        if self.current_token != None:
            raise CocalcException("Parser: Excess tokens, parser commited sudoku: ", self.current_token)

        return result

    def expr(self):
        """
        returns an expression tree, separates by addition and substraction
        """
        result = self.term()

        #check if expression is an assignment
        if (self.current_token != None) and (self.current_token.type == TokenType.ASSIGNMENT):
            self.advance()
            result = AssignmentNode(result, self.expr())
            return result

        #while current_token exists and is addition and substraction 
        while self.current_token != None and (self.current_token.type == TokenType.ARITH_OPERATION) and (self.current_token.value in (Values.AR_ADD, Values.AR_SUB)):
            # explore the terms inside
            if self.current_token.value == Values.AR_ADD:
                self.advance()
                result = ArithmeticNode('+', result, self.term())
            else:
                self.advance()
                result = ArithmeticNode('-', result, self.term())

        return result

    def term(self):
        """
        returns a term, separates by multiplication and division
        """
        result = self.exp_analysis()

        #while current_token exists and is multiplication and division
        while self.current_token != None and (self.current_token.type == TokenType.ARITH_OPERATION) and (self.current_token.value in (Values.AR_MUL, Values.AR_DIV)):
            # explore the factors inside
            if self.current_token.value == Values.AR_MUL:
                self.advance()
                result = ArithmeticNode('*', result, self.exp_analysis())
            else:
                self.advance()
                result = ArithmeticNode('/', result, self.exp_analysis())

        return result

    def exp_analysis(self):
        result = self.factor()

        #while current_token exists and is exponentiation
        while self.current_token != None and (self.current_token.type is TokenType.ARITH_OPERATION) and (self.current_token.value is Values.AR_EXP):
            self.advance()
            result = ArithmeticNode('^', result, self.factor())

        return result


    def factor(self):
        """
        returns nodes that can't be analyzed
        monomials
        """
        token = self.current_token

        #if token is call
        if token.type is TokenType.CALL:
            name = token.value
            args = []
            self.advance()
            while self.current_token.type != TokenType.PAREN and self.current_token.value != Values.PAREN_CLOSE:
                #security check
                if self.current_token == None:
                    raise CocalcException("Parser: Didn't close call parenthesis")
                args.append(self.factor())

            #pass the parenthesis
            self.advance()
            return CallNode(name, args)

        #if token opens parenthesis
        elif token.type is TokenType.PAREN and token.value is Values.PAREN_OPEN:
            self.advance()
            result = self.expr()

            #if parenthesis is not closed, user forgot to close it, raise exception
            if self.current_token.type != TokenType.PAREN or self.current_token.value != Values.PAREN_CLOSE:
                raise CocalcException("Parser: You didn't close the parenthesis")
            self.advance()
            return result

        #if token is number
        elif token.type in (TokenType.INT, TokenType.FLOAT):
            self.advance()
            return DataNode(token.value)

        #if token is symbol
        elif (token.type is TokenType.SYMBOL):
            self.advance()
            return DataNode(sympy.Symbol(token.value))

        #if token is varName
        elif (token.type == TokenType.VAR):
            self.advance()
            return VarNode(token.value)

        #if token is a unary (e.g.: the signs in -3 or +5)
        elif (token.type == TokenType.ARITH_OPERATION) and (token.value == Values.AR_SUB):
            self.advance()
            return UnaryNode('-', self.factor())
        elif (token.type == TokenType.ARITH_OPERATION) and (token.value == Values.AR_ADD):
            self.advance()
            return UnaryNode('+', self.factor())

        #if nothing was returned, then parser is not prepared to deal with the user intellect
        raise CocalcException("Parser: You commited an ucky wucky uwu. Check your syntax king")

