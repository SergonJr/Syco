from sly import Lexer

class BasicLexer(Lexer):
    tokens = {
        'ID',
        'INT',
        'FLOAT',
        'NAME',
        'IF',
        'THEN',
        'ELSE',
        'FOR',
        'TO',
        'WHILE',
        'ARROW',
        'COMMENT'
    }

    literals = { '=', '+', '-', '*', '/', '(', ')', ',', ';', '.', ' '}

    # Define tokens
    IF = r'if'
    THEN = r'then'
    ELSE = r'else'
    FOR = r'for'
    TO = r'to'
    WHILE = r'while'
    ARROW = r'->'
    ID = r'[a-zA-Z_][a-zA-Z_0-9]*'

    @_(r'\d+\.\d*')
    def FLOAT(self, x):
        x.value = float(x.value)
        return x

    @_(r'\d+')
    def INT(self, x):
        x.value = int(x.value)
        return x

    @_(r'//.*')
    def COMMENT(self, t):
        pass

    @_(r' ')
    def space(self, t):
        pass

    @_(r'\n+')
    def newline(self, t):
        self.lineno = t.value.count('\n')

if __name__ == '__main__':
    lexer = BasicLexer()
    env = {}
    while True:
        try:
            text = input('compiler > ')            
        except EOFError:
            break
        if text:
            lex = lexer.tokenize(text)
            for token in lex:
                print(token)