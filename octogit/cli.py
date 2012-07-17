"""
octogit

this file contains all the helper cli commands for octogit

"""
import os
import re
import sys
import requests

from clint import args
from clint.textui import colored, puts, indent

from .core import (get_issues, get_single_issue, create_repository,
                   close_issue, view_issue, create_issue, find_github_remote)
from .config import login, create_config, commit_changes, CONFIG_FILE


GIT_REPO_ENDPOINT = 'https://api.github.com/repos/%s/%s'

def version():
    from . import __version__
    return ".".join(str(x) for x in __version__)


def get_help():
    puts('{0}. version {1} by Mahdi Yusuf {2}'.format(
            colored.blue('octogit'),
            version(),
            colored.green('@myusuf3')))
    puts('{0}: http://github.com/myusuf3/octogit'.format(colored.yellow('source')))

    puts('\n{0}:'.format(colored.cyan('tentacles')))
    with indent(4):
        puts(colored.green('octogit login'))
        puts(colored.green("octogit create <repo> 'description'"))
        puts(colored.green("octogit create <repo> 'description' <organization>"))
        puts(colored.green('octogit issues [--assigned]'))
        puts(colored.green('octogit issues'))
        puts(colored.green("octogit issues create 'issue title' 'description'"))
        puts(colored.green('octogit issues <number>'))
        puts(colored.green('octogit issues <number> close'))
        puts(colored.green('octogit issues <number> view'))
        puts('\n')


def get_parent_repository(username_repo):
    username, repo = username_repo
    url = GIT_REPO_ENDPOINT % (username, repo)
    response = requests.get(url)
    data = response.json
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


def begin():
    if os.path.exists(CONFIG_FILE):
        pass
    else:
        # create config file
        create_config()
        # commit changes
        commit_changes()

    if args.flags.contains(('--version', '-v')):
        puts(version())
        sys.exit(0)

    elif args.get(0) == None:
        get_help()

    elif args.flags.contains(('--help', '-h')) or args.get(0) == 'help':
        get_help()
        sys.exit(0)

    elif args.get(0) == 'create':
        if args.get(1) == None:
            puts('{0}. {1}'.format(colored.blue('octogit'),
                colored.red('You need to pass both a project name and description')))

        else:
            project_name = args.get(1)
            description = args.get(2) or ''
            organization = args.get(3)
            create_repository(project_name, description, organization=organization)
            sys.exit()

    elif args.flags.contains(('--issues', '-i')) or args.get(0) == 'issues':
        url = find_github_remote()
        username, url = get_username_and_repo(url)
        if args.get(1) == 'create':
            if args.get(2) == None:
                puts('{0}. {1}'.format(colored.blue('octogit'),
                    colored.red('You need to pass an issue title')))
                sys.exit(-1)

            else:
                issue_name = args.get(2)
                description = args.get(3)
                create_issue(username, url, issue_name, description)
                sys.exit(0)

        issue_number = args.get(1)

        if issue_number is not None:
            if args.get(2) == 'close':
                close_issue(username, url, issue_number)
                sys.exit(0)
            elif args.get(2) == 'view':
                view_issue(username, url, issue_number)
                sys.exit(0)
            elif args.get(1) == '--assigned':
                get_issues(username, url, args.flags.contains(('--assigned', '-a')))
                sys.exit(0)
            else:
                get_single_issue(username, url, issue_number)
                sys.exit(0)
        else:
                get_issues(username, url, False)
                sys.exit(0)

    elif args.flags.contains(('--login', '-l')) or args.get(0) == 'login':
        username = args.get(1)
        if username is None:
            username = raw_input("Github username: ")
            if len(username) == 0:
                puts("{0}. {1}".format(
                        colored.blue("octogit"),
                        colored.red("Username was blank")))

        password = args.get(2)
        if password is None:
            import getpass
            password = getpass.getpass("Password for %s: " % username)

        login(username, password)
    else:
        get_help()
        sys.exit(0)
