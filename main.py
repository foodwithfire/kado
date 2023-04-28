import kado

while True:
    user_input = input("kado -> ")
    decryptor = kado.decryptor(user_input)
    result = ""
    for element in decryptor.decrypted:
        result += element
    print(f"-> {result}")
