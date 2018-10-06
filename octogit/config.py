import os
import sys

import requests

from clint.textui import colored, puts
from six.moves import configparser


try:
    import json
except ImportError:
    import simplejson as json  # NOQA

CONFIG_FILE = os.path.expanduser('~/.config/octogit/config.ini')
# ran the first time login in run
# config = configparser.ConfigParser()


def get_parser():
    try:
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)
    except Exception as e:
        puts(colored.red(
                "ERROR: Attempting to get config parser failed: {}".format(e)
            )
        )
        config = None
    return config


def commit_changes(config):
    """
    Write changes to the config file.
    """
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)


def create_config():
    """Create a configuration file for octogit."""
    if os.path.isfile(CONFIG_FILE):
        return
    # Make sure the path exists, and if it doesn't, create it.
    if not os.path.exists(os.path.dirname(CONFIG_FILE)):
        os.makedirs(os.path.dirname(CONFIG_FILE))
    # touch the config file.
    open(CONFIG_FILE, 'a').close()
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
    except configparser.NoOptionError:
        if get_username() == "":
            raise
        puts(colored.green(
            "We're just migrating your account from plaintext passwords to "
            "OAuth tokens"
        ))
        login(get_username(), config.get('octogit', 'password'))
        config.remove_option('octogit', 'password')
        puts(colored.green("Pretty spiffy huh?"))
        return config.get('octogit', 'token')


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
    payload = {
        "note": "octogit",
        "note_url": "https://github.com/myusuf3/octogit",
        "scopes": ["repo"]
    }
    response = requests.post(
        'https://api.github.com/authorizations',
        auth=(username, password),
        json=payload,
    )
    if response.status_code == 201:
        puts(colored.green('You have successfully been authenticated with Github'))
        data = json.loads(response.content)
        token = data["token"]
        set_username(username)
        set_token(token)
    elif response.status_code == 422:
        puts(colored.red('An access token already exists! Exiting...')) 
        sys.exit()
    else:
        msg = '{}. {}'.format(
            colored.blue('octogit'),
            colored.red('Do you even have a Github account? Bad Credentials')
        )
        puts(msg)
        sys.exit(3)

