DIGITS = "0123456789"

INTEGER = "INT"
FLOAT = "FLOAT"
PLUS = "PLUS"
MINUS = "MIN"
DIVIDE = "DIV"
MULTIPLY = "MUL"
ENDOFFILE = "EOF"


class Token:
    def __init__(self, type, value=None):
        self.value = value
        self.type = type
        self.format = f"[{self.type}]"
        if self.value != None:
            self.format += f": '{self.value}'"
        if self.type != ENDOFFILE:
            self.format += " | "


class Lexer:
    def __init__(self, user_input):
        self.tokens = []
        self.user_input = user_input
        self.current_char = ""
        self.pos = 0
        self.transform_to_token()
        self.token_type = None
        self.token_value = None

    def transform_to_token(self):
        error = False
        self.current_char = self.user_input[self.pos]
        while self.pos < len(self.user_input):
            if self.current_char in DIGITS:
                self.number = self.current_char
                while True:
                    if self.current_char in DIGITS and self.next_char() == 1:
                        self.number += self.current_char
                    else:
                        break
                self.token_type = INTEGER
                self.number_ = ""
                for digit in self.number:
                    if digit in DIGITS:
                        self.number_ += digit
                    else:
                        self.pos -= 1
                self.token_value = self.number_
            elif self.current_char == ".":
                self.token_type = FLOAT
            elif self.current_char == " ":
                self.next_char()
                continue
            elif self.current_char in "+-*/":
                self.token_value = None
                if self.current_char == "+":
                    self.token_type = PLUS
                elif self.current_char == "-":
                    self.token_type = MINUS
                elif self.current_char == "*":
                    self.token_type = MULTIPLY
                elif self.current_char == "/":
                    self.token_type = DIVIDE
            else:
                self.tokens = f"Error : Illegal character -> '{self.current_char}'"
                error = True
                break
            self.tokens.append(Token(self.token_type, self.token_value).format)
            self.next_char()

        if not error:
            self.tokens.append(Token(ENDOFFILE).format)

    def next_char(self):
        self.pos += 1
        try:
            self.current_char = self.user_input[self.pos]
            return 1
        except:
            return 0
