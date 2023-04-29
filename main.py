import kado

while True:
    user_input = input("kado -> ")
    lexer = kado.Lexer(user_input)
    result = ""
    for element in lexer.tokens:
        result += element
    print(f"-> {result}")
