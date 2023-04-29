# CONSTANTS ----------------------------------------------------------------------------------------

DIGITS = '0123456789'

# TOKENS DECLARATION -------------------------------------------------------------------------------

TOKEN_INT = "INT"
TOKEN_FLOAT = "FLOAT"
TOKEN_PLUS = "PLUS"
TOKEN_MINUS = "MINUS"
TOKEN_MUL = "MUL"
TOKEN_DIV = "DIV"
TOKEN_LPAREN = "LPAREN"
TOKEN_RPAREN = "RPAREN"
TOKEN_EOF = "EOF"

# TOKEN CLASS --------------------------------------------------------------------------------------

class Token:

    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value:
            return f'{self.type}:{self.value}'
        else:
            return f'{self.type}'

# POSITION CLASS -----------------------------------------------------------------------------------

class Position:

    def __init__(self, index, col, line, filename, filetext):
        self.index = index
        self.col = col
        self.line = line
        self.filename = filename
        self.filetext = filetext

    def pos_advance(self, current_char=None):
        self.index += 1
        self.col += 1
        if current_char == "\n":
            self.line += 1
            self.col = 0

    def copy(self):
        return Position(self.index, self.col, self.line, self.filename, self.filetext)

# LEXER CLASS --------------------------------------------------------------------------------------

class Lexer:

    def __init__(self, filename, text):
        self.filename = filename
        self.text = text
        self.pos = Position(-1, 0, -1, filename, text)
        self.current_char = None
        self.lexer_advance()

    def lexer_advance(self):
        self.pos.pos_advance()
        if self.pos.index < len(self.text):
            self.current_char = self.text[self.pos.index]
        else:
            self.current_char = None

    def get_tokens(self):
        tokens = []
        while self.current_char is not None:
            if self.current_char in " \t":
                self.lexer_advance()
            elif self.current_char in DIGITS:
                tokens.append(Token(self.get_number()))
                self.lexer_advance()
            elif self.current_char == "+":
                tokens.append(Token(TOKEN_PLUS))
                self.lexer_advance()
            elif self.current_char == "-":
                tokens.append(Token(TOKEN_MINUS))
                self.lexer_advance()
            elif self.current_char == "*":
                tokens.append(Token(TOKEN_MUL))
                self.lexer_advance()
            elif self.current_char == "/":
                tokens.append(Token(TOKEN_DIV))
                self.lexer_advance()
            elif self.current_char == "(":
                tokens.append(Token(TOKEN_LPAREN))
                self.lexer_advance()
            elif self.current_char == ")":
                tokens.append(Token(TOKEN_RPAREN))
                self.lexer_advance()
            else:
                char = self.current_char
                filename = self.filename
                line = self.pos.line
                self.lexer_advance()
                return [], IllegalCharError("'" + char + "'", filename, line)
        tokens.append(Token(TOKEN_EOF))
        return tokens, None

    def get_number(self):
        num_str = ''
        dot_count = 0
        while self.current_char is not None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1:
                    break
                else:
                    dot_count += 1
                    num_str += '.'
                    self.lexer_advance()
            else:
                num_str += self.current_char
                self.lexer_advance()
        if dot_count == 0:
            return Token(TOKEN_INT, int(num_str))
        else:
            return Token(TOKEN_FLOAT, float(num_str))

# ERROR CLASS --------------------------------------------------------------------------------------

class Error:

    def __init__(self, error_name, details, filename, line):
        self.error_name = error_name
        self.details = details
        self.filename = filename
        self.line = line

    def as_string(self):
        error = f'\033[0;31m{self.error_name}: {self.details} \n'
        error += f'File {self.filename}, at line {self.line + 1}\033[0m'
        return error

# CLASSES FOR ERRORS -------------------------------------------------------------------------------

class IllegalCharError(Error):

    def __init__(self, details, filename, line):
        super().__init__("IllegalCharacterError", details, filename, line)

# RUN ----------------------------------------------------------------------------------------------

def run(filename, text):
    lexer = Lexer(filename, text)
    tokens, error = lexer.get_tokens()
    return tokens, error
