#!/usr/bin/python

import os
from ConfigParser import SafeConfigParser

config = os.path.expander('~/.config/octogit/config.ini')

parser = SafeConfigParser()

try:
	parser.read(config)
except IOError:
	parser.write(config, '')
	parser.readfp(config)

# add octogit section if not present
if not parser.has_section('octogit'):
	parser.add_section('octogit')


