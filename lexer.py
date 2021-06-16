from enum import Enum
from tokens import TokenType, Token, Values
from calc_excepts import LexerException

BLANK = ' \n\t,'
DIGITS = '0123456789'
CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'
STRING_CHAR = '"'

class Lexer:
    """
    The lexer abstracts the characters into lexical units (Tokens)
    """
    def __init__(self, text):
        self.text = iter(text)
        self.advance()

    def advance(self):
        try:
            self.current_char = next(self.text)
        except StopIteration:
            self.current_char = None

    def generate_number(self):
        """
        returns TokenType.FLOAT if there is a decimal point:
            e.g.:
            1.3 -> TokenType.FLOAT = 1.3
            1. -> TokenType.FLOAT = 1.0
            .03 -> TokenType.FLOAT = 0.03

        otherwise TokenType.INT
        """
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

    def generate_str(self):
        """
        Generate a string token

        This is called just when a STRING_CHAR is found
        so it advances past STRING_CHAR and starts to read characters
        it stops when:
            1-There are no more characters to read,
            this raises an exception,
            as string was not closed

            2-self.current_char is STRING_CHAR,
            it doesn't append that character
            into the result.
            Then it advances so STRING_CHAR is disposed
        """
        self.advance()
        full_str = self.current_char
        self.advance()

        while self.current_char not in (None, STRING_CHAR):
            full_str += self.current_char
            self.advance()

        if self.current_char == None:
            raise LexerException("Lexer: Couldn't find string finisher")
        self.advance()

        return Token(TokenType.STRING, full_str)

    def generate_tokens(self):
        """
        Creates a generator that yields Tokens
        raises LexerException if a character can't
        be processed
        """
        while self.current_char != None:
            if self.current_char in BLANK:
                self.advance()
            #numbers
            elif self.current_char in DIGITS or self.current_char == '.':
                yield self.generate_number()

            #characters
            elif self.current_char in CHARS:
                yield self.generate_char_token()

            #parenthesis open
            elif self.current_char == '(':
                self.advance()
                yield Token(TokenType.PAREN, Values.PAREN_OPEN)
            #parenthesis close
            elif self.current_char == ')':
                self.advance()
                yield Token(TokenType.PAREN, Values.PAREN_CLOSE)
            #assignment
            elif self.current_char == '=':
                self.advance()
                yield Token(TokenType.ASSIGNMENT, None)
            #string
            elif self.current_char == STRING_CHAR:
                yield self.generate_str()

            ###### ARITHMETIC SYMBOLS #####
            #addition
            elif self.current_char == '+':
                self.advance()
                yield Token(TokenType.ARITH_OPERATION, Values.AR_ADD)
            #substraction
            elif self.current_char == '-':
                self.advance()
                yield Token(TokenType.ARITH_OPERATION, Values.AR_SUB)
            #division
            elif self.current_char == '/':
                self.advance()
                yield Token(TokenType.ARITH_OPERATION, Values.AR_DIV)
            #multiplication
            elif self.current_char == '*':
                self.advance()
                yield Token(TokenType.ARITH_OPERATION, Values.AR_MUL)
            #exponentiation
            elif self.current_char == '^':
                self.advance()
                yield Token(TokenType.ARITH_OPERATION, Values.AR_EXP)

            #lexer didn't understand what the user tried to say
            else:
                raise LexerException(f"Lexer: explain this -> {self.current_char}")


