class CocalcException(Exception):
    pass


class LexerException(CocalcException):
    pass


class ParserException(CocalcException):
    pass


class InterpreterException(CocalcException):
    pass


class EnvironmentException(CocalcException):
    pass


class MathError(CocalcException):
    pass
