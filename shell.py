import kado, os

while True:

    enter = input("Kado > ")
    if enter == "": continue
    result, error = kado.run("<stdin>", enter)

    if error:
        print(error.as_string())
    else:
        print(result)
