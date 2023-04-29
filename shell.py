import kado

while True:

    enter = input("Kado > ")
    result, error = kado.run("<stdin>", enter)

    if error:
        print(error.as_string())
    else:
        print(result)
