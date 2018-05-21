from helpers import compose

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
                    if strchar == '\\':
                        curr += codelist.pop(0)
                    else:
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
    """ lisp code -> AST in the form of a nested python list """
    return compose(
        code_to_tokens,
        tokens_to_ast
    )(code)
