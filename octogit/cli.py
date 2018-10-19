"""
octogit

this file contains all the helper cli commands for octogit

"""
import re

import requests

GIT_REPO_ENDPOINT = 'https://api.github.com/repos/%s/%s'


def version():
    from . import __version__
    return ".".join(str(x) for x in __version__)


def get_parent_repository(username_repo):
    username, repo = username_repo
    url = GIT_REPO_ENDPOINT % (username, repo)
    response = requests.get(url)
    data = response.json()
    try:
        parent = data['parent']['full_name']
        username_repo = parent.split('/')
    except KeyError:
        pass
    return username_repo


def get_username_and_repo(url):

    # matching origin of this type
    # http://www.github.com/myusuf3/delorean
    m = re.match("^.+?github.com/([a-zA-Z0-9_-]*)/([a-zA-Z0-9_-]*)\/?$", url)
    if m:
        return m.groups()
    else:
        # matching origin of this type
        # git@github.com:[/]myusuf3/delorean.git
        username_repo = url.split(':')[1].replace('.git', '').split('/')
        # Handle potential leading slash after :
        if username_repo[0] == '':
            username_repo = username_repo[1:]
        if len(username_repo) == 2:
            info = username_repo
        else:
            # matching url of this type
            # git://github.com/myusuf3/delorean.git
            username_repo = url.split('/')[3:]
            username_repo[1] = username_repo[1].replace('.git', '')
            info = username_repo
    parent_repo = get_parent_repository(info)
    return parent_repo
