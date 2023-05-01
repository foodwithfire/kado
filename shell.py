import kado, os

while True:

    enter = input("Kado > ")
    if enter == "": continue
    result, error = kado.run(os.path.basename(__file__), enter)

    if error:
        print(error.as_string())
    else:
        print(result)
