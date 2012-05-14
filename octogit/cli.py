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
        get_single_issue, create_repository, close_issue,
        view_issue, create_issue)
from .config import login, create_config, commit_changes, CONFIG_FILE


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


def git_status():
    print git.status()

def get_username_and_repo(url):
    username, reponame = extract_url_details(url)

    repo = get_repo_info(username, reponame)

    has_issues = repo.get('has_issues')
    fork = repo.get('fork')
    parent = repo.get('parent')

    if has_issues:
        return (username, reponame,)

    if fork and parent:
        parent_user = parent.get('owner', {}).get('login')
        if parent_user:
            return (parent_user, reponame)

    return (username, reponame,)



def extract_url_details(url):
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
        puts(version())
        sys.exit(0)

    elif args.get(0) == None:
        get_help()

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
            organization = args.get(3)
            create_repository(project_name, description, organization=organization)
            sys.exit()

    elif args.flags.contains(('--issues', '-i')) or args.get(0) == 'issues':
        repo = get_repository()
        url = find_github_remote(repo)
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

        issue_number = None
        try:
            issue_number = int(args.get(1))
        except:
            pass
        if issue_number is not None:
            if args.get(2) == 'close':
                close_issue(username, url, issue_number)
                sys.exit(0)
            elif args.get(2) == 'view':
                view_issue(username, url, issue_number)
                sys.exit(0)
            else:
                get_single_issue(username, url, issue_number)
                sys.exit(0)
        get_issues(username, url, args.flags.contains(('--assigned', '-a')))
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
