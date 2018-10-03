"""
octogit

this file contains all the helper cli commands for octogit

"""
import os
import re
import sys
import requests

from six.moves import input
from docopt import docopt
from clint.textui import colored, puts, indent

from .core import (get_issues, get_single_issue, create_repository,
                   close_issue, view_issue, create_issue, find_github_remote)
from .config import login, create_config, CONFIG_FILE


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


def begin():
    """
    Usage:
      octogit [subcommand] [arguments]
      octogit login | -l | --login [(username password)]
      octogit create <repo> [<description>] [<organization>]
      octogit (issues | -i | --issues) [--assigned | -a]
      octogit (issues | -i | --issues) create <issue-title> <description>
      octogit (issues | -i | --issues) <number> [close | view]
      octogit -v | --version
      octogit help | -h | --help

      """

    if os.path.exists(CONFIG_FILE):
        pass
    else:
        # create config file
        create_config()
        # commit changes (now this is called
        # automatically after create_config()
        # commit_changes()

    arguments = docopt(begin.__doc__, help=None)

    if arguments['--version'] or arguments['-v']:
        puts(version())
        sys.exit(0)

    elif arguments['--help'] or arguments['-h'] or arguments['help']:
        get_help()
        sys.exit(0)

    elif arguments['create']:
        if arguments['<repo>'] is None:
            puts('{0}. {1}'.format(colored.blue('octogit'),
                colored.red('You need to pass both a project name and description')))

        else:
            project_name = arguments['<repo>']
            description = arguments['<description>'] or ''
            organization = arguments['<organization>'] or None
            create_repository(project_name, description, organization=organization)
            sys.exit()

    elif arguments['--issues'] or arguments['-i'] or arguments['issues']:
        url = find_github_remote()
        username, url = get_username_and_repo(url)
        if arguments['create']:
            if ['<issue-title>'] is None:
                puts('{0}. {1}'.format(colored.blue('octogit'),
                    colored.red('You need to pass an issue title')))
                sys.exit(-1)

            else:
                issue_name = arguments['<issue-title>']
                description = arguments['<description>']
                create_issue(username, url, issue_name, description)
                sys.exit(0)

        issue_number = arguments['<number>']

        if issue_number is not None:
            if issue_number.startswith('#'):
                issue_number = issue_number[1:]

            if arguments['close']:
                close_issue(username, url, issue_number)
                sys.exit(0)
            elif arguments['view']:
                view_issue(username, url, issue_number)
                sys.exit(0)
            elif arguments['--assigned']:
                get_issues(username, url, (arguments['-assigned'] or arguments['-a']))
                sys.exit(0)
            else:
                get_single_issue(username, url, issue_number)
                sys.exit(0)
        else:
                get_issues(username, url, False)
                sys.exit(0)

    elif arguments['--login'] or arguments['-l'] or arguments['login']:
        username = arguments['username'] or None
        if username is None:
            username = input("Github username: ")
            if len(username) == 0:
                puts("{0}. {1}".format(
                        colored.blue("octogit"),
                        colored.red("Username was blank")))

        password = arguments['password'] or None
        if password is None:
            import getpass
            password = getpass.getpass("Password for %s: " % username)

        login(username, password)
    else:
        get_help()
        sys.exit(0)
