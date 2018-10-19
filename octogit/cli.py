"""
octogit

this file contains all the helper cli commands for octogit

"""
import os
import re
import sys
import requests

from docopt import docopt
from clint import args
from clint.textui import colored, puts, indent

from .core import (get_issues, get_single_issue, create_repository,
                   close_issue, view_issue, create_issue, find_github_remote)
from .config import login, create_config, commit_changes, CONFIG_FILE


def version():
    """Stringify the version tuple.

    :rtype: str
    """
    from . import __version__
    return ".".join(str(x) for x in __version__)


def get_help():
    """Generate a help output for the CLI command."""
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


def get_username_and_repo(url):
    """Parse the user name and repository from the given ``url``.

    There are 3 types of URLs we expect::

        1. http paths ("http://www.github.com/myusuf3/delorean")
        2. ssh paths ("git@github.com:[/]myusuf3/delorean")
        3. git protocol paths ("git:github.com/myusuf3/delorean.git")

    For each there is a regex expression to extract the user name and repository
    name from such an URL.

    :param str url: The URL to parse from.
    :rtype: Tuple[str, str]
    """
    # matching origin of this type
    # http://www.github.com/myusuf3/delorean
    web_addr = re.match("^.+?github.com/(?P<user>\w+)/(?P<repo>\w+)\/?$", url)
    ssh_addr = re.match(r"^.+github.com(:/|:)(?P<user>\w+)/(?P<repo>\w+)", url)
    git_prot_addr = re.match(r"^git://github.com/(?P<user>\w+)/(?P<repo>\w+)", url)
    for match in (web_addr, ssh_addr, git_prot_addr):
        if match:
            return match.group('user'), match.group('repo')


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
        if arguments['<repo>'] == None:
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
            if ['<issue-title>'] == None:
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
            username = raw_input("Github username: ")
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
