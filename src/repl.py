from helpers import compose
from parser import parse
from evaluator import evaluate

def serialize(expr):
    """ python list -> lisp code """
    if expr is None: return 'nil'
    if type(expr) is list:
        return '(' + ' '.join(serialize(x) for x in expr) + ')'
    return str(expr)

def interpret(code, lisp_output=False):
    """
    lisp code string, 
        lisp_output=True -> lisp code str
        lisp_output=False -> python list
    """
    steps = [parse, evaluate]
    if lisp_output: steps.append(serialize)
    return compose(*steps)(code)

def repl(code=None):
    """ interactive repl """
    if code:
        res = interpret('(do {})'.format(code), lisp_output=True)
        if res != 'nil': print res
    prompt = '> '
    print('(lisp-in-python)')
    while True:
        expr = raw_input(prompt)
        if expr in ('exit', 'quit'): break
        try:
            val = interpret(expr, lisp_output=True)
            print(val)
        except Exception as e:
            print('Error: {}'.format(e))
