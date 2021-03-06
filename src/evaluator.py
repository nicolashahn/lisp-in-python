from env import Env, builtin_map
from symbols import (
    _println,
    _quote, 
    _define, 
    _do,
    _lambda,
    _cond,
    _count
)

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

def serialize(expr):
    """ python list -> lisp code """
    if expr is None: return 'nil'
    if type(expr) is list:
        return '(' + ' '.join(serialize(x) for x in expr) + ')'
    return str(expr)

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
        if first == _println:
            serialized = [serialize(evaluate(e, env)) for e in rest]
            print(' '.join(serialized))
            return
        if first == _quote:
            return expr[1]
        if first == _define:
            (_, sym, val) = expr
            env[sym] = evaluate(val, env)
            return
        if first == _do:
            return [evaluate(x, env) for x in rest][-1]
        if first == _lambda:
            (_, params, body) = expr
            return Proc(params, body, env)
        if first == _cond:
            pairs = expr[1:]
            for cond, then in pairs:
                if evaluate(cond, env) is not False:
                    return evaluate(then, env)
            return evaluate(pairs[-1][1], env)
        if first == _count:
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
