from sly import Lexer
from sly import Parser

class BasicLexer(Lexer):
    tokens = {
        'FUN',
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
        'COMMENT',
        'STRING',
        'EQEQ'
    }

    literals = { '=', '+', '-', '*', '/', '(', ')', ',', ';', '.', ' '}

    # Define tokens
    FUN = r'function'
    IF = r'if'
    THEN = r'then'
    ELSE = r'else'
    FOR = r'for'
    TO = r'to'
    WHILE = r'while'
    ARROW = r'->'
    ID = r'[a-zA-Z_][a-zA-Z_0-9]*'
    STRING = r'\".*?\"'

    EQEQ = r'=='

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

class BasicParser(Parser):
    tokens = BasicLexer.tokens

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS'),           
    )

    def __init__(self):
        self.env = {}

    # Statements

    @_('')
    def statement(self, x):
        pass

    @_('FOR var_assign TO expr THEN statement')
    def statement(self, x):
        return ('for_loop', ('for_loop_setup', x.var_assign, x.expr), x.statement)

    @_('IF condition THEN statement ELSE statement')
    def statement(self, x):
        return ('if_stmt', x.condition, ('branch', x.statementA, x.statementB))

    @_('FUN ID "(" ")" ARROW statement')
    def statement(self, x):
        return ('fun_def', x.ID, x.statement)

    @_('ID "(" ")"')
    def statement(self, x):
        return ('fun_call', x.ID)
    
    @_('var_assign')
    def statement(self, x):
        return x.var_assign

    @_('expr')
    def statement(self, x):
        return (x.expr)

    # Conditions

    @_('expr EQEQ expr')
    def condition(self, x):
        return ('condition_eqeq', x.expr0, x.expr1)

    # Variable Assignment

    @_('ID "=" expr')
    def var_assign(self, x):
        return ('var_assign', x.ID, x.expr)

    @_('ID "=" STRING')
    def var_assign(self, x):
        return ('var_assign', x.ID, x.STRING)

    @_('expr "+" expr')
    def expr(self, x):
        return ('add', x.expr0, x.expr1)

    @_('expr "-" expr')
    def expr(self, x):
        return ('sub', x.expr0, x.expr1)

    @_('expr "*" expr')
    def expr(self, x):
        return ('mul', x.expr0, x.expr1)

    @_('expr "/" expr')
    def expr(self, x):
        return ('div', x.expr0, x.expr1)

    @_('"-" expr %prec UMINUS')
    def expr(self, x):
        return x.expr

    @_('ID')
    def expr(self, x):
        return ('var', x.ID)

    @_('INT')
    def expr(self, x):
        return ('int', x.INT)

    @_('FLOAT')
    def expr(self, x):
        return ('float', x.FLOAT)


if __name__ == '__main__':
    lexer = BasicLexer()
    parser = BasicParser()
    env = {}
    while True:
        try:
            text = input('compiler > ')            
        except EOFError:
            break
        if text:
            tree = parser.parse(lexer.tokenize(text))
            print(tree)