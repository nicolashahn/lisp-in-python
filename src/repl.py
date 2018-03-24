from helpers import compose
from env import Env, builtin_map

g_env = Env()

class Proc():
    """ user defined procedures """
    
    def __init__(self, params, body, env):
        self.params, self.body, self.env = params, body, env
    
    def __call__(self, *args):
        combined_env = Env(self.env)
        for k, v in zip(self.params, args):
            combined_env[k] = v
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
    if token[0] is '"':
        # just pop off " chars
        return token[1:-1]
    return token

def code_to_tokens(code):
    """ code:str -> flat token list """
    tokens = []
    curr = ''
    # if quote_parens > 0, we're inside a quoted list
    quote_parens = 0
    codelist = list(code)
    while codelist:
        char = codelist.pop(0)
        if char not in (';', '"', '(', ')', ' ', '\n', "'"):
            curr += char
        else:
            if char == "'":
                tokens += ['(', 'quote']
                quote_parens += 1
            if char == '"':
                curr += char
                while codelist:
                    strchar = codelist.pop(0)
                    curr += strchar
                    if strchar == '"':
                        break
            if char == ';':
                if curr: tokens.append(curr)
                curr = ''
                while codelist:
                    comchar = codelist.pop(0)
                    if comchar == '\n':
                        break
            if curr:
                tokens.append(curr)
            if char in ('(', ')'):
                if quote_parens and char is '(':
                    quote_parens += 1
                if quote_parens and char is ')':
                    quote_parens -= 1
                    if quote_parens == 1:
                        tokens.append(')')
                        quote_parens = 0
                tokens.append(char)
            curr = ''
    return tokens

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
            # pairs = zip(*(iter(rest),) * 2)
            pairs = expr[1:]
            for cond, then in pairs:
                if evaluate(cond, env) is not False:
                    return evaluate(then, env)
            return evaluate(pairs[-1][1], env)
        if first == 'count':
            (_, proc, l) = expr
            return reduce(lambda acc,i: acc + 1 if evaluate(proc, env)(i) else acc, l, 0)
        if first in env:
            first = env[first]
        # procedure call
        if callable(first):
            try:
                args = [evaluate(arg, env) for arg in rest]
                return first(*args)
            except Exception as e:
                print env.env_map
                print expr
                raise e
        if len(expr) == 1:
            return first
        return [evaluate(el, env) for el in expr]
    if [evaluate(el, env) for el in expr] == expr:
        return expr
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

def repl(code=None):
    """ interactive repl """
    if code:
        res = interpret('(do {})'.format(code), lisp_output=True)
        if res != 'nil': print res
    # all env vars that are not builtin
    # print [(k, g_env.env_map[k]) for k in g_env.env_map if k not in builtin_map]
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
