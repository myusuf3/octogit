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
# config = ConfigParser.ConfigParser()


def get_parser():
    try:
        config = ConfigParser.ConfigParser()
        config.read(CONFIG_FILE)
    except Exception as e:
        puts(colored.red("ERROR: Attempting to get config parser failed: {}".format(e)))
        config = None
    return config


def commit_changes(config):
    """
    Write changes to the config file.
    """
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)


def create_config():
    # If this returns False, file does not exist
    if os.path.isfile(CONFIG_FILE):
        pass
    else:
        # need an extra check here in cases where the path exists
        # but the file doesn't (if it was renamed)
        if not os.path.exists(os.path.dirname(CONFIG_FILE)):
            os.makedirs(os.path.dirname(CONFIG_FILE))
        open(CONFIG_FILE, 'w').close()
        config = get_parser()
        config.add_section('octogit')
        config.set('octogit', 'username', '')
        config.set('octogit', 'token', '')
        commit_changes(config)


def get_token():
    config = get_parser()    
    # Catch edgecase where user hasn't migrated to tokens
    try:
        return config.get('octogit', 'token')
    except ConfigParser.NoOptionError:
        if get_username() != "":
            puts(colored.green("We're just migrating your account from plaintext passwords to OAuth tokens"))
            login(get_username(), config.get('octogit', 'password'))
            config.remove_option('octogit', 'password')
            puts(colored.green("Pretty spiffy huh?"))
            return config.get('octogit', 'token')
        else:
            raise


def get_username():
    config = get_parser()    
    return config.get('octogit', 'username')


def get_headers(headers=()):
    defaults = {"Authorization": "token %s" % get_token()}
    defaults.update(headers)
    return defaults


def have_credentials():
    return get_username() != '' and get_token() != ''


def set_token(token):
    """
    Given a config set the token attribute
    in the Octogit section.
    """
    config = get_parser()
    config.set('octogit', 'token', token)
    commit_changes(config)


def set_username(username):
    """
    Given a config set the username attribute
    in the Octogit section.
    """
    config = get_parser()
    config.set('octogit', 'username', username)
    commit_changes(config)


def login(username, password):
    body = json.dumps({"note": "octogit",
                       "note_url": "https://github.com/myusuf3/octogit",
                       "scopes": ["repo"]})
    r = requests.post('https://api.github.com/authorizations',
                      auth=(username, password), data=body)
    if r.status_code == 201:
        puts(colored.green('You have successfully been authenticated with Github'))
        data = json.loads(r.content)
        token = data["token"]
        set_username(username)
        set_token(token)
    elif r.status_code == 422:
        puts(colored.red('An access token already exists! Exiting...')) 
        sys.exit()
    else:
        puts('{0}. {1}'.format(colored.blue('octogit'),
                               colored.red('Do you even have a Github account? Bad Credentials')))
        sys.exit(3)

