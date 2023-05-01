# GRAMMAR ------------------------------------------------------------------------------------------
"""
Grammar:
    expression = term (PLUS|MINUS) term
    term = factor (MUL|DIV) factor
    factor = INT|FLOAT

Objectif du Parser :
    Transformer les Tokens en un AST (Abstract Syntax Tree)
    Gérer les erreurs de syntaxe (ex : 2 + renverra une erreur)

KESKESÉ UN AST : (Admis Sans Travailler dans l'Interpréteur paske il fait r)
    Cé un truk qui dit en gros :
    Oké j'ai ces tokens là: INT:69, PLUS, INT:42, MUL, FLOAT:49.3
    KESKEJENFÉ???? ba dire dans quel ordre doit être quoi...
    Et il nous renverra cette magnifique chaîne de tokens:
    (INT:69, PLUS, (INT:42, MUL, FLOAT:49.3))
    Ce qui indiquera à notre povr interpréteur dans quel ordre faire quoi.

MAIS LE BOULOT DU PARSER NE S'ARRETE PAS LA !
Il doit aussi trouver, débusquer, TRAQUER les erreurs :
    Exemple simple :
    Les tokens sont : INT:69, PLUS, INT:42, MUL
    Si le parser ne trouvait pas le problème, il nous renverrait:
    (INT:69, PLUS, (INT:42, MUL))
    Et l'interpréteur lui, il se dirait :
        Alor jdois d'abord faire 42, le token c'est MUL, MAIS FOIS QUOI PTN
    et il nous renverrait une erreur :/

    Alors que là, le parser devrait nous renvoyer l'erreur lui-même, avant la katastrof:
    Si je reprends l'exemple :
    (INT:69, PLUS, (INT:42, MUL)) -> Analyz -> AAAAA y'a un MUL tout seul là le pauvre fo pa le laisser sans
    famille keskonvafèr aled osekour bon j'appuie sur la manette d'urgence

    InvalidSyntaxError: 69 + 42 * (Int or float expected)
    File <stdin>, at line 0

    Une autre erreur un peu spéciale MAIS importante à débusquer, c'est la division par zéro.

    (INT: 69, DIV, INT:0)

    Là le parser doit tout de suite dire: opla on passe paaaaaaaaa

    ArithmeticError: division by 0.
    File <stdin>, at line 0
"""

# CONSTANTS ----------------------------------------------------------------------------------------

DIGITS = '0123456789'

# TOKENS DECLARATION -------------------------------------------------------------------------------

TOKEN_INT = "INT"  # Nombre entier quelconque
TOKEN_FLOAT = "FLOAT"  # Nombre décimal quelconque
TOKEN_PLUS = "PLUS"  # Opérateur d'addition "+"
TOKEN_MINUS = "MINUS"  # Opérateur de soustraction "-"
TOKEN_MUL = "MUL"  # Opérateur de multiplication "*"
TOKEN_DIV = "DIV"  # Opérateur de division "/"
TOKEN_LPAREN = "LPAREN"  # Parenthèse gauche "("
TOKEN_RPAREN = "RPAREN"  # Parenthèse droite ")"
TOKEN_COMMENT = "COMMENT"  # Commentaires "//", "::", "##", '"""', "/* */"
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
                dot_count += 1
                num_str += '.'
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

# NODE CLASSES -------------------------------------------------------------------------------------

class NumberNode:

    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return f'{self.token}'

class BinOpNode:

    def __init__(self, left_node, operator_token, right_node):
        self.left_node = left_node
        self.operator_token = operator_token
        self.right_node = right_node

    def __repr__(self):
        return f'({self.left_node}, {self.operator_token}, {self.right_node}'

# PARSER CLASS -------------------------------------------------------------------------------------

class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = -1
        self.current_token = None
        self.parser_advance()

    def parser_advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        else:
            self.current_token = None
        return self.current_token

    """
    Rappel de la grammaire:
        expr = term ((PLUS|MINUS) term)*
        term = factor ((MUL|DIV) factor)*
        factor = INT|FLOAT
    """

    def factor(self):
        token = self.current_token
        print(token.type)
        if self.current_token.type == TOKEN_INT or self.current_token.type == TOKEN_FLOAT:
            self.parser_advance()
            return NumberNode(token)

    def term(self):
        return self.binary_operation(self.factor, (TOKEN_MUL, TOKEN_DIV))

    def expression(self):
        return self.binary_operation(self.term, (TOKEN_PLUS, TOKEN_MINUS))

    def binary_operation(self, func, ops):
        left_factor = func()
        while self.current_token in ops:
            operator_token = self.current_token
            self.parser_advance()
            right_factor = func()
            left_factor = BinOpNode(left_factor, operator_token, right_factor)
        return left_factor

    def parse(self):
        parsing_result = self.expression()
        print(parsing_result)
        return parsing_result

# CLASSES FOR ERRORS -------------------------------------------------------------------------------

class IllegalCharError(Error):

    def __init__(self, details, filename, line):
        super().__init__("IllegalCharacterError", details, filename, line)

# RUN ----------------------------------------------------------------------------------------------

def run(filename, text):
    lexer = Lexer(filename, text)
    tokens, error = lexer.get_tokens()
    if error:
        return None, error

    parser = Parser(tokens)
    ast = parser.parse()
    return ast, None
