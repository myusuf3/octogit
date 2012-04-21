"""
octogit

this file contains all the helper cli commands for octogit

"""
import os
import re
import sys

from pbs import git
from clint import args
from clint.textui import colored, puts, indent

from .core import (get_repository, get_issues,
        get_single_issue, create_repository, close_issue)
from .config import login, create_config, commit_changes, CONFIG_FILE


def get_help():
    puts('{0}.'.format(colored.blue('octogit')))
    puts('\n{0}:'.format(colored.cyan('tentacles')))
    with indent(4):
        puts(colored.green('octogit login'))
        puts(colored.green("octogit create <repo> 'description'"))
        puts(colored.green('octogit issues'))
        puts(colored.green('octogit issues <number>'))
        puts(colored.green('octogit issues <number> close'))
        puts('\n')

def show_boating():
    puts('{0}. version 0.1.3 by Mahdi Yusuf {1}'.format(colored.blue('octogit'), colored.green('@myusuf3')))
    puts('{0}: http://github.com/myusuf3/octogit'.format(colored.yellow('source')))

def version():
    show_boating()

def git_status():
    print git.status()

def get_username_and_repo(url):
    # matching origin of this type
    # http://www.github.com/myusuf3/delorean
    m = re.match("^.+?github.com/([a-zA-Z0-9_-]*)/([a-zA-Z0-9_-]*)\/?$", url)
    if m:
        return m.groups()
    else:
        # matching origin of this type
        # git@github.com:myusuf3/delorean.git
        username_repo = url.split(':')[1].replace('.git', '').split('/')
        if len(username_repo) == 2:
            return username_repo
        else:
            # matching url of this type
            # git://github.com/myusuf3/delorean.git
            username_repo = url.split('/')[3:]
            username_repo[1]=username_repo[1].replace('.git', '')
            return username_repo

def find_github_remote(repository):
    remotes = repository.remotes
    for remote in remotes:
        if 'github' in remote.url:
            return remote.url
        else:
            pass
    puts(colored.red('This repository has no Github remotes'))
    sys.exit(0)

def begin():
    if os.path.exists(CONFIG_FILE):
        pass
    else:
        # create config file
        create_config()
        # commit changes
        commit_changes()

    if args.flags.contains(('--version', '-v')):
        version()
        sys.exit(0)

    elif args.get(0) == None:
        show_boating()

    elif args.get(0) == 'status':
        git_status()
        sys.exit(0)

    elif args.flags.contains(('--help', '-h')) or args.get(0) == 'help':
        get_help()
        sys.exit(0)

    elif args.get(0) == 'create':
        if args.get(1) == None or args.get(2) == None:
            puts('{0}. {1}'.format(colored.blue('octogit'),
                colored.red('You need to pass both a project name and description')))

        else:
            project_name = args.get(1)
            description = args.get(2)
            create_repository(project_name, description)
            sys.exit()

    elif args.flags.contains(('--issues', '-i')) or args.get(0) == 'issues':
        repo = get_repository()
        url = find_github_remote(repo)
        username, url = get_username_and_repo(url)
        issue_number = None
        try:
            issue_number = int(args.get(1))
        except:
            pass
        if issue_number is not None:
            if args.get(2) == 'close':
                close_issue(username, url, issue_number)
                sys.exit(0)
            else:
                get_single_issue(username, url, issue_number)
                sys.exit(0)
        get_issues(username, url)
        sys.exit(0)

    elif args.flags.contains(('--login', '-l')) or args.get(0) == 'login' :
        if args.get(1) == None or args.get(2) == None:
            puts('{0}. {1}'.format(colored.blue('octogit'),
                colored.red('You need both a password and username to login')))
        else:
            username = args.get(1)
            password = args.get(2)
            login(username, password)
    else:
        get_help()
        sys.exit(0)


