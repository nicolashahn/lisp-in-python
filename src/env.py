import builtins as bi

builtin_map = {
    '+':            bi.add,
    '-':            bi.sub,
    '*':            bi.mult,
    '/':            bi.div,
    'eq?':          bi.is_eq,
    'cons':         bi.cons,
    'car':          bi.car,
    'cdr':          bi.cdr,
    'atom?':        bi.is_atom,
    'if':           bi.if_
}

class Env():
    ''' thin wrapper around dict, in order to handle scope '''

    def __init__(self, outer={}):
        self.env_map = builtin_map.copy()
        for k in outer:
            self.env_map[k] = outer[k]
    
    def __getitem__(self, k):
        return self.env_map[k]

    def __setitem__(self, k, v):
        self.env_map[k] = v

    def __contains__(self, k):
        return k in self.env_map
