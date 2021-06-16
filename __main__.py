from prettifier.colorifier import colorify, TextColor
from parser_ import Parser
from lexer import Lexer
from interpreter import Interpreter
from calc_excepts import CocalcException

prompt=colorify('cocalc > ', TextColor.OKCYAN)

interpreter = Interpreter()
while True:
    try:
        #### Read ####
        text = input(prompt)
        lexer = Lexer(text)
        tokens = lexer.generate_tokens()
        # print(list(tokens))

        #### Interpret ####
        parser = Parser(tokens)
        tree = parser.parse()
        # print(tree)
        value = interpreter.check(tree)

        #### Print ####
        print(colorify(f"\t= {value}", TextColor.OKGREEN))
    except CocalcException as e:
        print(colorify(e, TextColor.FAIL))

    except KeyboardInterrupt:
        print('Goodbye OwO')
        exit()

