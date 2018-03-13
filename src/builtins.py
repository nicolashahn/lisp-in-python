# core builtin lisp functions

from functools import reduce

# TODO the infix operators probably have equivalent 'math' stdlib functions
def add(*args):
    return reduce(lambda x, y: x + y, args)

def sub(*args):
    return reduce(lambda x, y: x - y, args)

def mult(*args):
    return reduce(lambda x, y: x * y, args)

def div(*args):
    return reduce(lambda x, y: x / y, args)

def is_eq(*args):
    for i in range(len(args) - 1):
        if args[i] != args[i+1]:
            return False
    return True

def cons(*args):
    return args

def car(arg):
    return arg[0]

def cdr(arg):
    return tuple(arg[1:])

def is_atom(arg):
    return type(arg) != list

def if_(cond_, then_, else_=None):
    return then_ if cond_ else else_
