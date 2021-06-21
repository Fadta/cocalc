import sympy
from tokens import Values, TokenType
from calc_excepts import ParserException
from nodes import *
from interpreter import Environment

#requires py >= 3.5
RESERVED_NAMES = [*Environment().builtin_functions] + [*Environment().variables]

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

        if there are excess tokens
        (i.e.: current_token != None at the end of analysis)
        raises ParserException
        """
        if self.current_token == None:
            return None

        result = self.assign_analysis()

        if self.current_token != None:
            raise ParserException("Parser: Excess tokens, parser commited sudoku: ", self.current_token)

        return result

    def assign_analysis(self):
        result = self.expr()
        res_type = type(result)
        assign_type = -1

        if res_type is VarNode: assign_type = 0
        elif res_type is CallNode: assign_type = 1

        if (self.current_token != None) and (self.current_token.type == TokenType.ASSIGNMENT):
            if result.name in RESERVED_NAMES:
                raise ParserException(f'Parser: name "{result.name}" is reserved')
            self.advance()
            if assign_type == 1:
                result = FuncAssignNode(result, self.expr())
                result.link_variables()
            elif assign_type == 0:
                result = AssignmentNode(result, self.expr())

        return result


    def expr(self):
        """
        returns an expression tree, separates by addition and substraction
        """
        result = self.term()

        #check if expression is an assignment
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

    def extract_func_args(self):
        """
        Builds the argument part of a function call
        """
        args = []
        arg_count = 0
        self.advance()
        #Case: input non closing parenthesis: cocalc > function(
        while self.current_token is not None and self.current_token.type != TokenType.PAREN and self.current_token.value != Values.PAREN_CLOSE:
            #security check
            if self.current_token == None:
                raise ParserException("Parser: Didn't close call parenthesis")

            args.append(FuncParameter(str(arg_count), self.expr()))
            arg_count += 1
        if self.current_token is None: raise ParserException("Parser: Non closing parenthesis")

        #pass the closing parenthesis
        self.advance()
        return args


    def factor(self):
        """
        returns nodes that can't be analyzed
        monomials
        """
        token = self.current_token

        #if token opens parenthesis
        if token.type is TokenType.PAREN and token.value is Values.PAREN_OPEN:
            self.advance()
            #Case: input empty parenthesis: cocalc > (
            if self.current_token is None: raise ParserException("Parser: Non closing parenthesis")
            result = self.expr()

            #if parenthesis is not closed, user forgot to close it, raise exception
            if self.current_token is None or self.current_token.type != TokenType.PAREN or self.current_token.value != Values.PAREN_CLOSE:
                raise ParserException("Parser: You didn't close the parenthesis")
            self.advance()
            return result

        #if token is call
        elif token.type is TokenType.CALL:
            name = token.value
            args = self.extract_func_args()
            #self.advance()
            #Case: input non closing parenthesis: cocalc > function(
            #if self.current_token is None: raise ParserException("Parser: Non closing parenthesis")
            #while self.current_token.type != TokenType.PAREN and self.current_token.value != Values.PAREN_CLOSE:
                #security check
            #    if self.current_token == None:
            #        raise ParserException("Parser: Didn't close call parenthesis")
            #    args.append(self.factor())

            #pass the closing parenthesis
            #self.advance()
            return CallNode(name, args)

        #if token is number
        elif token.type in (TokenType.INT, TokenType.FLOAT):
            self.advance()
            return DataNode(token.value)

        #if token is symbol
        elif (token.type is TokenType.SYMBOL):
            self.advance()
            return DataNode(sympy.Symbol(token.value))

        elif token.type is TokenType.STRING:
            self.advance()
            return StringNode(token.value)

        #if token is varName
        elif (token.type == TokenType.VAR):
            self.advance()
            return VarNode(token.value, 0)

        #if token is a unary (e.g.: the signs in -3 or +5)
        elif (token.type == TokenType.ARITH_OPERATION) and (token.value == Values.AR_SUB):
            self.advance()
            return UnaryNode('-', self.factor())
        elif (token.type == TokenType.ARITH_OPERATION) and (token.value == Values.AR_ADD):
            self.advance()
            return UnaryNode('+', self.factor())

        #if nothing was returned, then parser is not prepared to deal with the user intellect
        raise ParserException(f"Parser({token}): You commited an ucky wucky uwu. Check your syntax king")

