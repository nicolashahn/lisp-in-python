from helpers import compose
from env import Env

g_env = Env()

class Proc():
    """ user defined procedures """
    
    def __init__(self, params, body, env):
        self.params, self.body, self.env = params, body, env
    
    def __call__(self, *args):
        combined_env = Env(dict(zip(self.params, args)))
        return evaluate(self.body, combined_env)


def token_to_num(token):
    return float(token) if '.' in token else int(token)

def token_to_atom(token):
    """ token str -> primitive/symbol """
    if token is 'nil': return None
    if token == 'true': return True
    if token == 'false': return False
    if token[0] in '1234567890':
        return token_to_num(token)
    # TODO support strings
    # elif token[0] in ('"',"'"):
        # return token_to_str(token)
    else:
        return token

def code_to_tokens(code):
    """ code:str -> flat token list """
    # TODO something will have to be done here to support strings w/spaces
    return (code.
        replace(',', ' ').
        # add spaces so split() separates correctly:
        #   bad: '(a)' -> ['(a)']
        #   good: ' ( a ) ' -> ['(', 'a', ')']
        replace('(', ' ( ').
        replace(')', ' ) ').
        split())

def tokens_to_ast(tokens):
    """ flat list including '(', ')' -> nested list without '(', ')' """
    res = []
    while tokens:
        token = tokens.pop(0)
        if token == ')': 
            return res
        elif token == '(': 
            res.append(tokens_to_ast(tokens))
        else:
            res.append(token_to_atom(token))
    # when tokens empty exit top level list, makes this reusable recursively
    return res[0]

def parse(code):
    return compose(
        code_to_tokens,
        tokens_to_ast
    )(code)

def evaluate(expr, env=g_env):
    """ evaluate expression to value recursively """
    if type(expr) != list or expr == []:
        if expr in env:
            return env[expr]
        return expr
    first = expr[0]
    if type(first) != list:
        # special cases
        rest = expr[1:]
        if first == 'println':
            serialized = [serialize(evaluate(e, env)) for e in rest]
            print(' '.join(serialized))
            return
        if first == 'quote':
            return expr[1]
        if first == 'define':
            (_, sym, val) = expr
            env[sym] = evaluate(val, env)
            return
        if first == 'do':
            return [evaluate(x, env) for x in rest][-1]
        if first == 'lambda':
            (_, params, body) = expr
            return Proc(params, body, env)
        if first == 'cond':
            pairs = zip(*(iter(rest),) * 2)
            for cond, then in pairs:
                if evaluate(cond, env) is not False:
                    return evaluate(then, env)
            return evaluate(pairs[-1][1], env)
        if first in env:
            first = env[first]
        # procedure call
        if callable(first):
            args = [evaluate(arg, env) for arg in rest]
            return first(*args)
        if len(expr) == 1:
            return first
        return [evaluate(el, env) for el in expr]
    return evaluate([evaluate(el, env) for el in expr], env)

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

def repl():
    """ interactive repl """
    prompt = '> '
    print('lisp-in-python')
    while True:
        expr = raw_input(prompt)
        if expr in ('exit', 'quit'): break
        try:
            val = interpret(expr, lisp_output=True)
            print(val)
        except Exception as e:
            print('Error: {}'.format(e))
