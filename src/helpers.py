from functools import reduce

def compose(*fns):
    """ compose(f,g,h)(x) == h(g(f(x))) """
    return lambda x: reduce(lambda val, fn: fn(val), fns, x)
