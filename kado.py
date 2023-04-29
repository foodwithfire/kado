digits = "0123456789"

integer = "INT"
float = "FLOAT"
plus = "PLUS"
minus = "MIN"
divide = "DIV"
multiply = "MUL"
endoffile = "EOF"


class Token:
    def __init__(self, type, value=None):
        self.value = value
        self.type = type
        self.format = f"[{self.type}]"
        if self.value != None:
            self.format += f" - '{self.value}'"
        if self.type != endoffile:
            self.format += " | "


class Decryptor:
    def __init__(self, user_input):
        self.decrypted = []
        self.user_input = user_input
        self.current_char = ""
        self.pos = 0
        self.decrypt()
        self.token_type = None
        self.token_value = None

    def decrypt(self):
        while self.pos < len(self.user_input):
            self.current_char = self.user_input[self.pos]

            if self.current_char in digits:
                self.token_type = integer
                self.token_value = self.current_char
            elif self.current_char == " ":
                self.next_char()
                continue
            elif self.current_char in "+-*/":
                self.token_value = None
                if self.current_char == "+":
                    self.token_type = plus
                elif self.current_char == "-":
                    self.token_type = minus
                elif self.current_char == "*":
                    self.token_type = multiply
                elif self.current_char == "/":
                    self.token_type = divide
            else:
                self.decrypted = f"Error : Illegal character -> '{self.current_char}'"
                break
            self.decrypted.append(Token(self.token_type, self.token_value).format)
            self.next_char()

        if type(self.decrypted) == "<class 'list'>":
            self.decrypted.append(Token(endoffile).format)

    def next_char(self):
        self.pos += 1
        self.current_char = ""
