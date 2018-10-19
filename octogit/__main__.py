"""Run octogit from CLI.

Creates a parser object with several subcommands, which implement octogit's
functionality.

The parser tree looks as follows::

    octogit
    ├── login {username} {password}
    │
    ├── create {repository}
    │   │
    │   ├── -d | --description
    │   └──  -o | --organisation
    │
    └── issues
        │
        ├── list [-a | --assigned]
        ├── close {issue-number}
        ├── view {issue-number}
        └── create {title}
            │
            └──  -d | --description
"""
import os
import argparse
from config import CONFIG_FILE, create_config, login
from cli import version
from core import (
    get_issues,
    get_single_issue,
    create_repository,
    close_issue,
    view_issue,
    create_issue,
    find_github_remote,
    get_username_and_repo,
)

base_parser = argparse.ArgumentParser(
    prog="octogit", epilog="Version {} by Mahdi Yusuf @myusuf".format(version())
)


sub_parsers = base_parser.add_subparsers()

# Build Login parser
login_parser = sub_parsers.add_parser("login")
login_parser.add_argument("username", action='store', help="Your Github username.")
login_parser.add_argument("password", action='store', help="Your Github password.")

# Build create parser for repository creation.
create_parser = sub_parsers.add_parser("create")
create_parser.add_argument("repository", action='store')
create_parser.add_argument("--description", nargs=1, action='store', default="")
create_parser.add_argument("--organisation", nargs=1, action='store', default="")

# Build issues parser and subparsers
issues_parser = sub_parsers.add_parser("issues")
issues_subparsers = issues_parser.add_subparsers()

# Enale Listing issues (one specific one or all available)
issues_list_parser = issues_subparsers.add_parser("list")
issues_list_parser.add_argument("-a", "--assigned", action="store_true", default=False)

issues_close_parser = issues_subparsers.add_parser("close")
issues_close_parser.add_argument('issue')

issues_view_parser = issues_subparsers.add_parser("view")
issues_view_parser.add_argument('issue')

issues_create_parser = issues_subparsers.add_parser("create")
issues_create_parser.add_argument('title', action='store')
issues_create_parser.add_argument('--description', nargs=1, action='store')

options = base_parser.parse_args()


if not os.path.exists(CONFIG_FILE):
    create_config()

if options.create:
    project_name = options.repository
    description = options.descriptions
    organization = options.organization
    create_repository(project_name, description, organization=organization)
elif options.issues:
    url = find_github_remote()
    username, url = get_username_and_repo(url)
    if options.create:
        title = options.title
        description = options.description
        create_issue(username, url, title, description)
    elif options.list:
        get_issues(username, url, options.assigned)
    elif options.view:
        view_issue(username, url, options.issue)
    elif options.close:
        close_issue(username, url, options.issue)
    else:
        get_issues(username, url, False)
elif options.login:
    username = options.username
    password = options.password
    login(username, password)
