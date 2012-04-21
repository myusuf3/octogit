import os
import sys
import ConfigParser

import requests
from clint.textui import colored, puts, indent, columns

CONFIG_FILE = os.path.expanduser('~/.config/octogit/config.ini')
# ran the first time login in run
config = ConfigParser.ConfigParser()

def commit_changes():
    '''
    Write changes to the config file.
    '''
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

def create_config():
    if os.path.exists(CONFIG_FILE):
         pass
    else:
        os.makedirs(os.path.dirname(CONFIG_FILE))
        open(CONFIG_FILE, 'w').close()
        config.add_section('octogit')
        config.set('octogit', 'username', '')
        config.set('octogit', 'password', '')
        return config

def get_password():
    config.read(CONFIG_FILE)
    return config.get('octogit', 'password')

def get_username():
    config.read(CONFIG_FILE)
    return config.get('octogit', 'username')

def set_password(password):
    '''
    Given a config set the password attribute
    in the Octogit section.
    '''
    config.set('octogit', 'password', password)
    commit_changes()


def set_username(username):
    '''
    Given a config set the username attribute
    in the Octogit section.
    '''
    config.set('octogit', 'username', username)
    commit_changes()


def login(username, password):
    r = requests.get('https://api.github.com', auth=(username, password))
    if r.status_code == 200:
        puts(colored.green('You have successfully been authenticated with Github'))
    else:
        puts('{0}. {1}'.format(colored.blue('octogit'),
            colored.red('Do you even have a Github account? Bad Credentials')))
        sys.exit(3)


    if get_username() == username:
        pass
    else:
        set_username(username)

    if get_password() == password:
        pass
    else:
        set_password(password)

