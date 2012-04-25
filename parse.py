import ply.lex as lex
import sys

class SmallerSmallaLexer(object):
    reserved = {
        'if' : 'IF',
        'or' : 'OR',
        'and': 'AND',
        'not': 'NOT',
        'true': 'TRUE',
        'false': 'FALSE',
        'fact': "FACT",
    }

    tokens = [
            'NUMBER',
            'PLUS',
            'MINUS',
            'MULT',
            'LPAREN',
            'RPAREN',
    ] + list(reserved.values())

    t_PLUS    = r'\+'
    t_MINUS   = r'-'
    t_MULT   = r'\*'
    t_FACT = r'!'
    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'

    def t_NUMBER(self,t):
        r'-?\d+'
        t.value = int(t.value)
        return t

    # Tokens for reserved words.
    def t_RESERVED(self,t):
        r'\w+'
        t.type = self.reserved.get(t.value)
        if t.type == 'TRUE':
            t.value = 'true'
        elif t.type == 'FALSE':
            t.value = 'false'
        return t

    t_ignore = ' \t\n'

    t_ignore_COMMENT = r'\#.*'

    def t_error(self,t):
        print "Illegal character '%s'" % t.value[0]
        t.lexer.skip(1)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

print "Lexing..."
l = SmallerSmallaLexer()
l.build()
l.lexer.input(sys.argv[1])

#for tok in l.lexer:
#    print tok

# Parser
import ply.yacc as yacc
import ssast

tokens = l.tokens
class SmallerSmallaParser(object):
    def __init__(self, tokenlist):
        self.tokens = tokenlist

    def p_expression_plus(self, p):
        'expression : LPAREN PLUS expression expression RPAREN'
        p[0] = ssast.Expr(ssast.BinOp(ssast.Op('Plus'), p[3], p[4]))

    def p_expression_mult(self, p):
        'expression : LPAREN MULT expression expression RPAREN'
        p[0] = ssast.Expr(ssast.BinOp(ssast.Op('Mult'), p[3], p[4]))

    def p_expression_minus(self, p):
        'expression : LPAREN MINUS expression expression RPAREN'
        p[0] = ssast.Expr(ssast.BinOp(ssast.Op('Minus'), p[3], p[4]))

    def p_expression_or(self, p):
        'expression : LPAREN OR expression expression RPAREN'
        p[0] = ssast.Expr(ssast.BinOp(ssast.Op('Or'), p[3], p[4]))

    def p_expression_and(self, p):
        'expression : LPAREN AND expression expression RPAREN'
        p[0] = ssast.Expr(ssast.BinOp(ssast.Op('And'), p[3], p[4]))

    def p_expression_if(self, p):
        'expression : LPAREN IF expression expression expression RPAREN'
        p[0] = ssast.Expr(ssast.If(p[3], p[4], p[5]))

    def p_expression_fact(self, p):
        'expression : LPAREN FACT expression RPAREN'
        p[0] = ssast.Expr(ssast.UnaOp(ssast.Op('Fact'), p[3]))

    def p_expression_not(self, p):
        'expression : LPAREN NOT expression RPAREN'
        p[0] = ssast.Expr(ssast.UnaOp(ssast.Op('Not'), p[3]))

    def p_expression_int(self, p):
        'expression : NUMBER'
        p[0] = ssast.Expr(ssast.Val(ssast.Int(p[1])))

    def p_expression_boolean(self, p):
        '''expression : TRUE
                      | FALSE'''
        p[0] = ssast.Expr(ssast.Val(ssast.Boolean(p[1])))

    def p_error(self, p):
        print >> sys.stderr, "ERROR: Syntax error. Parser face-planted on this token: %s" % p

    def build(self, **kwargs):
        return yacc.yacc(module=self, **kwargs)

print "Parsing..."
parser = SmallerSmallaParser(l.tokens).build()

ast = parser.parse(sys.argv[1])
if ast:
    print ast

print "Writing program..."
itemplate = open("InterpTemplate.smalla").read()
open(sys.argv[2], 'w').write(itemplate % ast)
