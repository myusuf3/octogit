import os
import sys
import ConfigParser

import requests
from clint.textui import colored, puts

try:
    import json
except ImportError:
    import simplejson as json  # NOQA

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
        config.set('octogit', 'token', '')
        return config


def get_token():
    config.read(CONFIG_FILE)
    return config.get('octogit', 'token')


def get_username():
    config.read(CONFIG_FILE)
    return config.get('octogit', 'username')

def get_headers(headers=()):
    defaults = {"Authorization": "token %s" % get_token()}
    defaults.update(headers)
    return defaults

def have_credentials():
    get_username() != '' and get_token() != ''

def set_token(token):
    '''
    Given a config set the token attribute
    in the Octogit section.
    '''
    config.set('octogit', 'token', token)
    commit_changes()


def set_username(username):
    '''
    Given a config set the username attribute
    in the Octogit section.
    '''
    config.set('octogit', 'username', username)
    commit_changes()


def login(username, password):
    body = json.dumps({ "note": "octogit",
                        "note_url": "https://github.com/myusuf3/octogit",
                        "scopes": ["repo"]})
    r = requests.post('https://api.github.com/authorizations',
            auth=(username, password), data=body)
    if r.status_code == 201:
        puts(colored.green('You have successfully been authenticated with Github'))
    else:
        puts('{0}. {1}'.format(colored.blue('octogit'),
            colored.red('Do you even have a Github account? Bad Credentials')))
        sys.exit(3)
    data = json.loads(r.content)
    token = data["token"]

    if get_username() == username:
        pass
    else:
        set_username(username)

    if get_token() == token:
        pass
    else:
        set_token(token)
