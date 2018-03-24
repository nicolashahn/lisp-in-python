import repl
import sys

if __name__ == '__main__':
    if len(sys.argv) == 1:
        repl.repl()
    elif len(sys.argv) == 2:
        filename = sys.argv[1]
        with open(filename, 'r') as f:
            code = f.read()
            print repl.repl(code=code)
