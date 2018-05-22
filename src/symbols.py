class Symbol(str): pass

def Sym(s, symbol_table={}):
    "Find or create unique Symbol entry for str s in symbol table."
    if s not in symbol_table: symbol_table[s] = Symbol(s)
    return symbol_table[s]

_quote, _define, _lambda, _begin, _defmacro, = map(Sym, 
"quote   define   lambda   begin   defmacro".split())

_quasiquote, _unquote, _unquotesplicing = map(Sym,
"quasiquote   unquote   unquote-splicing".split())

_println, _do, _cond, _count = map(Sym, 
"println   do   cond   count".split())
