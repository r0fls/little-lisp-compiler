import comp
import sys
import readline

def repl():
    while True:
        try:
            exec(comp.compiler(raw_input('!~~ ')))
        except KeyboardInterrupt:
            print('\n')
            sys.exit()
        else:
            continue

if __name__ == "__main__":
    repl()
