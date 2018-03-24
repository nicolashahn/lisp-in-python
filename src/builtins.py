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

def greater_than(x,y):
    return x > y

def less_than(x,y):
    return x < y

def list_(*args):
    return list(args)

def cons(*args):
    return [args[0]] + args[1]

def car(arg):
    return arg[0]

def cdr(arg):
    return arg[1:]

def is_atom(arg):
    return type(arg) != list

def if_(cond_, then_, else_=None):
    return then_ if cond_ else else_

def str_concat(*args):
    return ''.join(args)

def list_ref(list_, i):
    return list_[i]

def str_split(string, sep):
    return string.split(sep)

def str_to_num(string):
    if '.' in string:
        return float(string)
    return int(string)

def length(arg):
    return len(arg)
