import builtins as bi

builtin_map = {
    '+':                bi.add,
    '-':                bi.sub,
    '*':                bi.mult,
    '/':                bi.div,
    'equal?':           bi.is_eq,
    '>':                bi.greater_than,
    '<':                bi.less_than,
    'cons':             bi.cons,
    'car':              bi.car,
    'cdr':              bi.cdr,
    'atom?':            bi.is_atom,
    'if':               bi.if_,
    'string-append':    bi.str_concat,
    'list-ref':         bi.list_ref,
    'str-split':        bi.str_split,
    'str->num':         bi.str_to_num,
    'length':           bi.length,
    'list':             bi.list_
}

class Env():
    ''' thin wrapper around dict, in order to handle scope '''

    def __init__(self, parent=None):
        self.parent = parent
        self.env_map = {}
        if not parent:
            self.env_map = builtin_map.copy()
    
    def __getitem__(self, k):
        if k in self.env_map:
            return self.env_map[k]
        else:
            return self.parent.env_map[k]

    def __setitem__(self, k, v):
        self.env_map[k] = v

    def __contains__(self, k):
        if type(k) in (tuple, list): return False
        if k in self.env_map: return True
        if self.parent:
            if k in self.parent.env_map: return True
