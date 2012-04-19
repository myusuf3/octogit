import os
import ConfigParser


def commit_changes(config):
    '''
    Write changes to the config file. 
    '''
    pass

def create_config():
    # ran the first time login in run
    if os.path.exists(octogit_config):
        pass
    else:
        os.makedirs(os.path.dirname(octogit_config))
        open(octogit_config, 'w').close()
        config = ConfigParser.ConfigParser()
        config.add_section('octogit')


def set_password(config, password):
    '''
    Given a config set the password attribute
    in the Octogit section. 
    '''
    pass

def set_username(config, username):
    '''
    Given a config set the username attribute
    in the Octogit section. 
    '''
    pass


def login():
    octogit_config = os.path.expanduser('~/.config/octogit/config.ini')

    config.set('octogit', 'user', '15')
    with open(octogit_config, 'w') as configfile:
        config.write(configfile)
