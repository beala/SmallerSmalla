import ply.lex as lex
import sys

# Parser
reserved = {
    'if' : 'IF',
    'or' : 'OR',
    'and': 'AND',
    'not': 'NOT',
    'true': 'TRUE',
    'false': 'FALSE',
}

tokens = [
        'NUMBER',
        'PLUS',
        'MINUS',
        'MULT',
        'FACT',
        'LPAREN',
        'RPAREN',
] + list(reserved.values())

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_MULT   = r'\*'
t_FACT = r'!'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

def t_NUMBER(t):
    r'-?\d+'
    t.value = int(t.value)
    return t

# Tokens for reserved words.
def t_RES(t):
    r'\w+'
    t.type = reserved.get(t.value)
    if t.type == 'TRUE':
        t.value = 'true'
    elif t.type == 'FALSE':
        t.value = 'false'
    return t

t_ignore = ' \t\n'

t_ignore_COMMENT = r'\#.*'

def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

print "Lexing..."
lexer = lex.lex()

lexer.input(sys.argv[1])

for tok in lexer:
    print tok

# Parser
import ply.yacc as yacc
import ssast

def p_expression_plus(p):
    'expression : LPAREN PLUS expression expression RPAREN'
    p[0] = ssast.Expr(ssast.BinOp(ssast.Op('Plus'), p[3], p[4]))

def p_expression_mult(p):
    'expression : LPAREN MULT expression expression RPAREN'
    p[0] = ssast.Expr(ssast.BinOp(ssast.Op('Mult'), p[3], p[4]))

def p_expression_minus(p):
    'expression : LPAREN MINUS expression expression RPAREN'
    p[0] = ssast.Expr(ssast.BinOp(ssast.Op('Minus'), p[3], p[4]))

def p_expression_or(p):
    'expression : LPAREN OR expression expression RPAREN'
    p[0] = ssast.Expr(ssast.BinOp(ssast.Op('Or'), p[3], p[4]))

def p_expression_and(p):
    'expression : LPAREN AND expression expression RPAREN'
    p[0] = ssast.Expr(ssast.BinOp(ssast.Op('And'), p[3], p[4]))

def p_expression_if(p):
    'expression : LPAREN IF expression expression expression RPAREN'
    p[0] = ssast.Expr(ssast.If(ssast.Expr(p[3]), ssast.Expr(p[4]), ssast.Expr(p[5])))

def p_expression_fact(p):
    'expression : LPAREN FACT expression RPAREN'
    p[0] = ssast.Expr(ssast.UnaOp(ssast.Op('!'), p[3]))

def p_expression_not(p):
    'expression : LPAREN NOT expression RPAREN'
    p[0] = ssast.Expr(ssast.UnaOp(ssast.Op('Not'), p[3]))

def p_expression_int(p):
    'expression : NUMBER'
    p[0] = ssast.Expr(ssast.Val(ssast.Int(p[1])))

def p_expression_boolean(p):
    '''expression : TRUE
                  | FALSE'''
    p[0] = ssast.Expr(ssast.Val(ssast.Boolean(p[1])))

def p_error(p):
    print >> sys.stderr, "ERROR: Syntax error. Parser face-planted on this token: %s" % p

print "Parsing..."
parser = yacc.yacc()

ast = parser.parse(sys.argv[1])
if ast:
    print ast

print "Writing program..."
itemplate = open("InterpTemplate.smalla").read()
open(sys.argv[2], 'w').write(itemplate % ast)
