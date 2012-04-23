# AST Nodes:
class Node(object):
    pass
class Expr(Node):
    def __init__(self, expr):
        self.expr = expr
    def __repr__(self):
        return "Expr(%s)" % (self.expr)
    def __str__(self):
        return "fold[Expr](inj[ExprUf](%s))" % (self.expr)
class BinOp(Node):
    def __init__(self, op, l, r):
        self.l = l
        self.op = op
        self.r = r
    def __repr__(self):
        return "BinOp(%s, %s, %s)" % (self.val, self.op, self.expr)
    def __str__(self):
        return "Binary:{op:inj[Op](%s:()), l:%s, r:%s}" % (self.op, self.l, self.r)
class UnaOp(Node):
    def __init__(self, op, l):
        self.op = op
        self.l = l;
    def __repr__(self):
        return "UnaOp(%s, %s)" % (self.op, self.l)
    def __str__(self):
        return "Unary:{op:inj[Op](%s:()), l:%s}" % (self.op, self.l)
class Val(Node):
    def __init__(self, val):
        self.val = val
    def __repr__(self):
        return "Val(%s)" % self.val
    def __str__(self):
        return "Val:inj[Val](%s)" % self.val
class Int(Node):
    def __init__(self,i):
        self.i = i
    def __repr__(self):
        return "Int(%d)" % self.i
    def __str__(self):
        return "I:%d" % self.i
class Op(Node):
    def __init__(self, op):
        self.op = op
    def __repr__(self):
        return "Op('%s')" % self.op
    def __str__(self):
        return self.op
class ParseError(Exception):
    def __init__(self, actual, expect):
        self.actual = actual
        self.expect = expect
    def __str__(self):
        return "Parse Error: expected '%s' but got '%s'" % (self.expected, self.actual)