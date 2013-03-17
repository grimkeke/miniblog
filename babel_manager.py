#!flask/bin/python
import os
import sys

if sys.platform == 'wn32':
    pybabel = 'flask\\Scripts\\pybabel'
else:
#    pybabel = 'flask/bin/pybabel'
    pybabel = 'pybabel'

def babel_init():
    os.system(pybabel + ' extract -F babel.cfg -k lazy_gettext -o messages.pot app')
    os.system(pybabel + ' init -i messages.pot -d app/translations -l ' + sys.argv[1])
    os.unlink('messages.pot')

def babel_update():
    os.system(pybabel + ' extract -F babel.cfg -k lazy_gettext -o messages.pot app')
    os.system(pybabel + ' update -i messages.pot -d app/translations')
    os.unlink('messages.pot')

def babel_compile():
    os.system(pybabel + ' compile -d app/translations')

def print_usage():
    print """Usage: python %s  [-iuc]
    -i | --init    babel_init
    -u | --update  babel_update
    -c | --compile babel_compile""" % sys.argv[0]

def main():
    if len(sys.argv) != 2:
        print_usage()
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd in ['-i', '--init']:
        babel_init()
    elif cmd in ['-u', '--update']:
        babel_update()
    elif cmd in ['-c', '--compile']:
        babel_compile()
    else:
        print_usage()

if __name__ == '__main__':
    main()
