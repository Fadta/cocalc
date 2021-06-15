from parser_ import Parser
from lexer import Lexer
from calc_excepts import CocalcException

while True:
    try:
        #### Read ####
        text = input('cocalc > ')
        lexer = Lexer(text)
        tokens = lexer.generate_tokens()

        #### Interpret ####
        parser = Parser(tokens)
        tree = parser.parse()

        #### Print ####
        print(tree, end='\n\n')
    except CocalcException as e:
        print(e)

    except KeyboardInterrupt:
        print('Goodbye OwO')
        exit()

