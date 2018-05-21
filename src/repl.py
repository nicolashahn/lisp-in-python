import cmd
import sys
from collections import deque

from helpers import compose
from parser import parse
from evaluator import evaluate

class CmdParse(cmd.Cmd):
    """using Cmd so repl can use line history"""

    commands = []
    prompt = '> '

    def emptyline(line):
        """if not overridden, sends last non-empty command"""
        pass
    
    def default(self, line):
        if line in ('exit', 'quit'): sys.exit()
        try:
            val = interpret(line, lisp_output=True)
            print(val)
        except Exception as e:
            print('Error: {}'.format(e))
        self.commands.append(line)

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
    # this is currently more FP than necessary, but will allow injecting
    # more steps easily in the future
    steps = [parse, evaluate]
    if lisp_output: steps.append(serialize)
    return compose(*steps)(code)

def repl(code=None):
    """ interactive repl """
    if code:
        res = interpret('(do {})'.format(code), lisp_output=True)
        if res != 'nil': print res
    history = deque(maxlen=100)
    prompt = '> '
    print('(lisp-in-python)')
    CmdParse().cmdloop()
