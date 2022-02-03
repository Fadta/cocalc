from cocalc.prettifier.colorifier import colorify, TextColor
from cocalc.parser_ import Parser
from cocalc.lexer import Lexer
from cocalc.interpreter import Interpreter, Environment
from cocalc.calc_excepts import CocalcException


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


def main():
    prompt = colorify('cocalc > ', TextColor.OKCYAN)
    env = Environment()

    #################################
    #        MAIN LOOP
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


if __name__ == "__main__":
    main()
