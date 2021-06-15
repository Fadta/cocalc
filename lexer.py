from enum import Enum
from tokens import TokenType, Token, Values

BLANK = ' \n\t,'
DIGITS = '0123456789'
CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'

class Lexer:
    def __init__(self, text):
        self.text = iter(text)
        self.advance()

    def advance(self):
        try:
            self.current_char = next(self.text)
        except StopIteration:
            self.current_char = None

    def generate_number(self):
        decimal_points = 0
        num_str = ''

        while (self.current_char != None) and ((self.current_char == '.') or (self.current_char in DIGITS)):
            if self.current_char == '.':
                decimal_points += 1
                if decimal_points > 1:
                    break;

            num_str += self.current_char
            self.advance()

        if decimal_points != 0:
            return Token(TokenType.FLOAT, float(num_str))
        else:
            return Token(TokenType.INT, int(num_str))

    def generate_char_token(self):
        """
        Read characters and return the adequate Token

        e.g.:
        if 'x' then it is algebraic symbol x
        if 'floor(' then it is call for function floor
        if 'gravity' then call for stored value: gravity
        """
        char_count = 1
        name = self.current_char
        isCall = False
        self.advance()

        while self.current_char != None and ((self.current_char in CHARS) or ( self.current_char == '(')):
            if self.current_char == '(':
                isCall = True
                self.advance()
                break
            name += self.current_char
            char_count += 1
            self.advance()

        if char_count == 1:
            return Token(TokenType.SYMBOL, name) #if 'x' then it is algebraic symbol x
        elif isCall:
            return Token(TokenType.CALL, name) #if 'floor(' then it is call for function floor
        else:
            return Token(TokenType.VAR, name) #if 'gravity' then call for stored value: gravity

    def generate_tokens(self):
        """
        Creates a generator that yields Tokens
        """
        while self.current_char != None:
            if self.current_char in BLANK:
                self.advance()
            elif self.current_char in DIGITS or self.current_char == '.':
                yield self.generate_number()

            elif self.current_char in CHARS:
                yield self.generate_char_token()

            elif self.current_char == '(':
                self.advance()
                yield Token(TokenType.PAREN, Values.PAREN_OPEN)
            elif self.current_char == ')':
                self.advance()
                yield Token(TokenType.PAREN, Values.PAREN_CLOSE)

            ###### ARITHMETIC SYMBOLS #####
            elif self.current_char == '+':
                self.advance()
                yield Token(TokenType.ARITH_OPERATION, Values.AR_ADD)
            elif self.current_char == '-':
                self.advance()
                yield Token(TokenType.ARITH_OPERATION, Values.AR_SUB)
            elif self.current_char == '/':
                self.advance()
                yield Token(TokenType.ARITH_OPERATION, Values.AR_DIV)
            elif self.current_char == '*':
                self.advance()
                yield Token(TokenType.ARITH_OPERATION, Values.AR_MUL)
            elif self.current_char == '^':
                self.advance()
                yield Token(TokenType.ARITH_OPERATION, Values.AR_EXP)

            else:
                raise Exception(f"IllegalCharacter: {self.current_char}")


