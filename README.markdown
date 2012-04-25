##SmallerSmalla##
###Description###
This is an interpreter for SmallerSmalla, a (very) small lisp-like language implemented in Smalla, with the parser implemented in Python. Smalla is a programming language specified by Professor Bor-Yuh Chang for a Principles of Programming Languages class at the Uni of Colorado for the Spring 2012 semester.

###Usage###
Parse a SmallerSmalla program:

```
python parse.py "(+ 1 1)" one-plus-one.smalla
```

This outputs a Smalla program to `one-plus-one.smalla` which adds `1` and `1`.

Run the program:

```
./ssrun one-plus-one.smalla
```

You may need to increase the memory allotted to the JVM. This sets the max at 4 gigabytes:

```
export JAVA_OPTS="-Xmx4G"
```

###Syntax and Semantics###
The syntax of SmallerSmalla is s-expressions, like lisp.

```
EXPR ::= (BINOP EXPR EXPR) |
         (UNARYOP EXPR)    |
         (if EXPR EXPR EXPR) |
         VAL
BINOP   ::= +|-|*|or|and
UNARYOP ::= !|not
VAL  ::= INT | BOOLEAN
INT  ::= ...-2|-1|0|1|2...
BOOLEAN ::= true | false
```

Example:

This adds `1` and `1` if `~(true and false)` is true (it is) otherwise it adds `2` and `1`.

```
(if (not (and true false)) (+ 1 1) (+ 2 1))
```

###Credits###
Bor-Yuh Chang wrote most of the Smalla implementation (`smalla.jar`)

The [PLY package](http://www.dabeaz.com/ply/ply.html) was used for parsing.
