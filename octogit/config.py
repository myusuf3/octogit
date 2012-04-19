import os
import ConfigParser

def set_password():
	pass


def set_username():
	pass


def login():
	octogit_config = os.path.expanduser('~/.config/octogit/config.ini')

	# ran the first time login in run
	if os.path.exists(octogit_config):
		pass
	else:
		os.makedirs(os.path.dirname(octogit_config))
		open(octogit_config, 'w').close()

	config = ConfigParser.ConfigParser()
	config.read(octogit_config)
	config.add_section('octogit')
	config.set('octogit', 'int', '15')
	with open(octogit_config, 'w') as configfile:
		config.write(configfile)