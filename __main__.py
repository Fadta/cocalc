from prettifier.colorifier import colorify, TextColor
from parser_ import Parser
from lexer import Lexer
from interpreter import Interpreter, Environment
from calc_excepts import *

def evaluate(environment, text):
    lexer = Lexer(text)
    tokens = lexer.generate_tokens()

    parser = Parser(tokens)
    tree = parser.parse()

    interpreter = Interpreter(environment)
    result = interpreter.check(tree)

    if type(result) in (int, float):
        environment.variables['ans'] = result

    return result

prompt=colorify('cocalc > ', TextColor.OKCYAN)
env = Environment()

#################################
######### MAIN LOOP
#################################
while True:
    try:
        text = input(prompt)

        value = evaluate(env, text)

        print(colorify(f"\t= {value}", TextColor.OKGREEN))

    except CocalcException as e:
        print(colorify(e, TextColor.FAIL))

    except KeyboardInterrupt:
        print('\nGoodbye OwO')
        exit()

