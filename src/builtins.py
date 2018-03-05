# core builtin lisp functions

from functools import reduce

# TODO the infix operators probably have equivalent 'math' lib functions
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

def quote(*args):
    # TODO
    pass

def cons(*args):
    return args

def car(arg):
    return arg[0]

def cdr(arg):
    return tuple(arg[1:])

def is_atom(arg):
    # TODO
    pass

def define(var, expr):
    # TODO
    pass

def _lambda(*args):
    # TODO
    pass

def cond(*args):
    # TODO
    pass

def _if(_cond, _then, _else):
    return _then if (_cond) else _else

builtin_map = {
    # normal form
    '+': add,
    '-': sub,
    '*': mult,
    '/': div,
    # special form
    'eq?': is_eq,
    'quote': quote,
    'cons': cons,
    'car': car,
    'cdr': cdr,
    'atom?': is_atom,
    'define': define,
    'lambda': _lambda,
    'cond': cond,
    # not part of core in Python Practice Projects assignment
    'if': _if
}


