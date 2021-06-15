from lexer import Lexer

while True:
    text = input('cocalc > ')
    lexer = Lexer(text)
    tokens = lexer.generate_tokens()
    print(list(tokens))

