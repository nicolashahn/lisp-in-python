import sys

from helpers import compose
from builtins import *

def token_to_num(token):
    return float(token) if '.' in token else int(token)

# def token_to_str(token):
    # if token[0] == '"':
        # return token.replace('"','')
    # elif token[0] == "'":
        # return token.replace("'",'')

def token_to_atom(token):
    """ token str -> builtin/primitive/symbol """
    if token in builtin_map:
        return builtin_map[token]
    elif token[0] in '1234567890':
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

def tokens_to_token_tree(tokens):
    """ flat list including '(', ')' -> nested list without '(', ')' """
    res = []
    while tokens:
        token = tokens.pop(0)
        if token == ')': 
            return res
        elif token == '(': 
            res.append(tokens_to_token_tree(tokens))
        else:
            res.append(token)
    # when tokens empty exit top level list, makes this reusable recursively
    return res[0]

def token_tree_to_ast(tree):
    """ nested list with token strs -> nested list with atoms """
    if tree == []: return []
    res = []
    while tree:
        token = tree.pop(0)
        if type(token) is list:
            res.append(token_tree_to_ast(token))
        else:
            res.append(token_to_atom(token))
    return res

def parse(code):
    return compose(
        code_to_tokens,
        tokens_to_token_tree,
        token_tree_to_ast,
    )(code)

def evaluate(expr):
    """ evaluate expression to value recursively """
    if type(expr) != list or expr == []:
        return expr
    first = expr[0]
    if type(first) != list:
        if first in builtin_map.values():
            fn, raw_args = first, expr[1:]
            args = [evaluate(arg) for arg in raw_args]
            return fn(*args)
        return [evaluate(el) for el in expr]
    return evaluate([evaluate(el) for el in expr])

def interpret(code):
    return compose(
        parse,
        evaluate,
        # TODO should this return a string of output of lisp program, or actual value?
        # str
    )(code)

if __name__ == '__main__':

    # read from file
    # TODO?

    # read from args
    print(interpret(sys.argv[1]))
    
    # read from stdin
    # NOTE: needs to be quoted
    # print(interpret(input()))
