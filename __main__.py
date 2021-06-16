from parser_ import Parser
from lexer import Lexer
from interpreter import Interpreter
from calc_excepts import CocalcException

interpreter = Interpreter()
while True:
    try:
        #### Read ####
        text = input('cocalc > ')
        lexer = Lexer(text)
        tokens = lexer.generate_tokens()
        # print(list(tokens))

        #### Interpret ####
        parser = Parser(tokens)
        tree = parser.parse()
        # print(tree)
        value = interpreter.check(tree)

        #### Print ####
        print('\t= ', value)
    except CocalcException as e:
        print(e)

    except KeyboardInterrupt:
        print('Goodbye OwO')
        exit()

