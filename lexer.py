from rply import LexerGenerator

TK_VAR =        "TK_VAR"
TK_OPEN_P =     "TK_OPEN_P"
TK_CLOSE_P =    "TK_CLOSE_P"
TK_PLUS =       "TK_PLUS"
TK_MINUS =      "TK_MINUS"
TK_MULT =       "TK_MULT"
TK_DIV =        "TK_DIV"
TK_ASSIGN =     "TK_ASSIGN"
TK_FUN =        "TK_FUN"
TK_RETURN =     "TK_RETURN"
TK_END =        "TK_END"
TK_COMMA =      "TK_COMMA"
TK_ID =         "TK_ID"
TK_NUMBER =     "TK_NUMBER"
TK_OPEN_BR =    "TK_OPEN_BR"
TK_CLOSE_BR =   "TK_CLOSE_BR"

class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        # palavras reservadas
        self.lexer.add(TK_VAR, r'var')
        self.lexer.add(TK_FUN, r'fun')
        self.lexer.add(TK_RETURN, r'return')
        self.lexer.add(TK_END, r';')
        self.lexer.add(TK_COMMA, r',')

        # parenteses
        self.lexer.add(TK_OPEN_P, r'\(')
        self.lexer.add(TK_CLOSE_P, r'\)')
        self.lexer.add(TK_OPEN_BR, r'\{')
        self.lexer.add(TK_CLOSE_BR, r'\}')

        # operadores
        self.lexer.add(TK_PLUS, r'\+')
        self.lexer.add(TK_MINUS, r'\-')
        self.lexer.add(TK_MULT, r'\*')
        self.lexer.add(TK_DIV, r'\/')
        self.lexer.add(TK_ASSIGN, r'\=')

        # identificador
        self.lexer.add(TK_ID, r'[a-zA-Z]+')

        # numero
        self.lexer.add(TK_NUMBER, r'[0-9]+')

        # ignora espaços
        self.lexer.ignore('\s+')

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()