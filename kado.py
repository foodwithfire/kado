digits = "0123456789"

integer = "INT"
float = "FLOAT"
plus = "PLUS"
minus = "MIN"
divide = "DIV"
multiply = "MUL"

class Token:
    def __init__(self, type, value=None):
        self.value = value
        self.type = type
        self.format = f"[{self.type}]"
        if self.value != None:
            self.format += f"->'{self.value}'"
        self.format += " | "

class decryptor:
    def __init__(self, user_input):
        self.decrypted = []
        self.user_input = user_input
        self.current_char = ""
        self.pos = 0
        self.decrypt()
       
    def decrypt(self):
        while self.pos < len(self.user_input):
            self.current_char = self.user_input[self.pos]
            
            if self.current_char in digits:
                self.type = integer
                self.value = self.current_char
            elif self.current_char == " ":
                self.next_char()
                continue
            elif self.current_char in "+-*/":
                self.value = None
                if self.current_char == "+":
                    self.type = plus
                elif self.current_char == "-":
                    self.type = minus
                elif self.current_char == "*":
                    self.type = multiply
                elif self.current_char == "/":
                    self.type = divide
            else:

                    self.decrypted = f"Error : Illegal character -> '{self.current_char}'"
                    break                    
            self.token = Token(self.type, self.value)
            self.decrypted.append(self.token.format)
            self.next_char()
       
    def next_char(self):
        self.pos += 1
        self.current_char = ""
