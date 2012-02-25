"""
hub

this file contains all the helper cli commands for hub

"""
import sys

from clint import args
from clint.textui import colored, puts, indent


def help():
	puts('How to hub:')
	with indent(4):
		puts(colored.cyan('hub create <repo>'))
		puts(colored.cyan('hub delete <repo>'))
		puts(colored.cyan('hub pull <repo>'))

def version():
	puts('development 0.0.1')

def show_boating():
	puts('{0} by Mahdi Yusuf <@myusuf3>'.format(colored.yellow('hub')))
	puts('{0} http://github.com/myusuf3/hub'.format(colored.yellow('source')))


def begin():
	if args.flags.contains(('--version', '-v')):
		version()
		sys.exit(0)

	elif args.get(0) == None:
		show_boating()

	elif args.flags.contains(('--help', '-h')):
		help()
		sys.exit(0)