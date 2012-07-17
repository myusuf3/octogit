# -*- coding: utf-8 -*-
"""
octogit

This file contains stuff for github api
"""

import os
import io
import re
import sys
import subprocess
import webbrowser
import requests
from clint.textui import colored, puts, columns

from .config import get_username, get_password

try:
    import json
except ImportError:
    import simplejson as json  # NOQA


ISSUES_ENDPOINT = 'https://api.github.com/repos/%s/%s/issues?page=%s'
CREATE_ISSUE_ENDPOINT = 'https://api.github.com/repos/%s/%s/issues'
SINGLE_ISSUE_ENDPOINT = 'https://api.github.com/repos/%s/%s/issues/%s'
ISSUES_PAGE = 'https://github.com/%s/%s/issues'
SINGLE_ISSUE_PAGE = 'https://github.com/%s/%s/issues/%s'

UPDATE_ISSUE = 'https://api.github.com/repos/%s/%s/issues/%s'


def valid_credentials():
    r = requests.get('https://api.github.com', auth=(get_username(), get_password()))
    if r.status_code == 200:
        return True
    else:
        return False


def push_to_master():
    cmd = ['git', 'push', '-u', 'origin', 'master']
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.communicate()


def create_octogit_readme():
    with io.open('README.rst', 'w') as fp:
        fp.write(u"""========
Octogit
========

This repository has been created with Octogit.

.. image:: http://myusuf3.github.com/octogit/assets/img/readme_image.png

Author
======
Mahdi Yusuf (@myusuf3)
""")


def git_init(repo_name):
    cmd = ["git", "init", repo_name]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.communicate()


def git_add_remote(username, repo_name):
    url = "git@github.com:%s/%s.git" % (username, repo_name)
    cmd = ["git", "remote", "add", "origin", url]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.communicate()


def git_initial_commit():
    cmd = ["git", "commit", "-am", "this repository now with more tentacles care of octogit"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.communicate()


def git_add():
    cmd = ["git", "add", "README.rst"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.communicate()


def local_already(repo_name):
    # mkdir repo_name
    if os.path.exists('/'.join([os.getcwd(), repo_name])):
        puts('{0}. {1}'.format(colored.blue('octogit'),
            colored.red('the repository already exists locally.')))
        return True
    else:
        return False


def create_local_repo(username, repo_name):
    # mkdir repo_name
    if os.path.exists('/'.join([os.getcwd(), repo_name])):
        puts('{0}. {1}'.format(colored.blue('octogit'),
            colored.red('the repository already exists locally.')))
    else:
        os.makedirs('/'.join([os.getcwd(), repo_name]))
        # cd repo_name
        os.chdir('/'.join([os.getcwd(), repo_name]))
        #git init
        git_init(os.getcwd())
        # create readme
        create_octogit_readme()
        # add readme
        git_add()
        #initial commit
        git_initial_commit()
        # add remote
        git_add_remote(username, repo_name)
        # push to master
        push_to_master()
        puts('{0}. {1}'.format(colored.blue('octogit'),
            colored.green('this is your moment of glory; Be a hero.')))


def close_issue(user, repo, number):
    if get_username() == '' or get_password() == '':
        puts('{0}. {1}'.format(colored.blue('octogit'),
            colored.red('in order to create a repository, you need to login.')))
        sys.exit(-1)
    update_issue = UPDATE_ISSUE % (user, repo, number)
    post_dict = {'state': 'close'}
    username = get_username()
    password = get_password()
    r = requests.post(update_issue, auth=(username, password), data=json.dumps(post_dict))
    if r.status_code == 200:
        puts('{0}.'.format(colored.red('closed')))
    else:
        puts('{0}. {1}'.format(colored.blue('octogit'),
            colored.red("You either aren't allowed to close repository or you need to login in silly.")))
        sys.exit(-1)


def view_issue(user, repo, number):
    """
    Displays the specified issue in a browser
    """

    github_view_url = SINGLE_ISSUE_PAGE % (user, repo, number)
    webbrowser.open(github_view_url)


def create_repository(project_name, description, organization=None):
    if get_username() == '' or get_password() == '':
        puts('{0}. {1}'.format(colored.blue('octogit'),
            colored.red('in order to create a repository, you need to login.')))
        sys.exit(1)

    if local_already(project_name):
        sys.exit(1)
    post_dict = {'name': project_name, 'description': description, 'homepage': '', 'private': False, 'has_issues': True, 'has_wiki': True, 'has_downloads': True}
    username = get_username()
    password = get_password()
    if organization:
        post_url = 'https://api.github.com/orgs/{0}/repos'.format(organization)
    else:
        post_url = 'https://api.github.com/user/repos'
    r = requests.post(post_url, auth=(username, password), data=json.dumps(post_dict))
    if r.status_code == 201:
        if organization:
            create_local_repo(organization, project_name)
        else:
            create_local_repo(username, project_name)
    else:
        # Something went wrong
        post_response = json.loads(r.content)
        errors = post_response.get('errors')
        if errors and errors[0]['message'] == 'name already exists on this account':
            puts('{0}. {1}'.format(colored.blue('octogit'),
                colored.red('repository named this already exists on github')))
        else:
            puts('{0}. {1}'.format(colored.blue('octogit'),
                colored.red('something went wrong. perhaps you need to login?')))
            sys.exit(-1)


def find_github_remote():
    cmd = ["git", "remote", "-v"]

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, sterr = proc.communicate()

    if not stdout:
        puts('{0}. {1}'.format(colored.blue('octogit'),
            colored.red('You need to be inside a valid git repository.')))
        sys.exit(0)

    remotes = stdout.strip().split('\n')
    for line in remotes:
        name, url, _ = line.split()
        if 'github.com' in url and name == 'origin':
            return url
    else:
        puts(colored.red('This repository has no Github remotes'))
        sys.exit(0)


def description_clean(string):
    new_string = ''
    for line in string.split('\n'):
        if line.strip():
            new_string += line + '\n'
    return new_string


def get_single_issue(user, repo, number):
    url = SINGLE_ISSUE_ENDPOINT % (user, repo, number)
    github_single_url = SINGLE_ISSUE_PAGE % (user, repo, number)
    puts('link. {0} \n'.format(colored.green(github_single_url)))
    if valid_credentials():
        connect = requests.get(url, auth=(get_username(), get_password()))
    else:
        connect = requests.get(url)

    issue = json.loads(connect.content)
    width = [[colored.yellow('#'+str(issue['number'])), 5],]
    width.append([colored.red('('+ issue['user']['login']+')'), 15])
    puts(columns(*width))
    description = description_clean(issue['body'])
    puts(description)


def get_issues(user, repo, assigned=None):
    github_issues_url = 'https://api.github.com/repos/%s/%s/issues' % (user, repo)

    params = None
    if assigned:
        params = {'assignee': user}

    link = requests.head(github_issues_url).headers.get('Link', '=1>; rel="last"')
    last = lambda url: int(re.compile('=(\d+)>; rel="last"$').search(url).group(1)) + 1

    for pagenum in xrange(1, last(link)):
        connect = requests.get(github_issues_url + '?page=%s' % pagenum, params=params)

        try:
            data = json.loads(connect.content)
        except ValueError:
            raise ValueError(connect.content)

        if not data:
            puts('{0}. {1}'.format(colored.blue('octogit'),
                colored.cyan('Looks like you are perfect welcome to the club.')))
            break

        elif 'message' in data:
            puts('{0}. {1}'.format(colored.blue('octogit'),
                                   colored.red(data['message'])))
            sys.exit(1)

        for issue in data:
            #skip pull requests
            if issue['pull_request']['html_url']:
                continue
            width = [[colored.yellow('#'+str(issue['number'])), 4],]
            if isinstance(issue['title'], unicode):
                issue['title'] = issue['title'].encode('utf-8')
            width.append([issue['title'], 80])
            width.append([colored.red('('+ issue['user']['login']+')'), None])
            print columns(*width)


def create_issue(user, repo, issue_name, description):
    username = get_username()
    password = get_password()

    if username == '' or password == '':
        puts('{0}. {1}'.format(colored.blue('octogit'),
            colored.red('in order to create an issue, you need to login.')))
        sys.exit(1)

    post_url = CREATE_ISSUE_ENDPOINT % (user, repo)
    post_dict = {'title': issue_name, 'body': description}

    r = requests.post(post_url, auth=(username, password), data=json.dumps(post_dict))
    if r.status_code == 201:
        puts('{0}. {1}'.format(colored.blue('octogit'),
            colored.red('New issue created!')))
    else:
        puts('{0}. {1}'.format(colored.blue('octogit'),
            colored.red('something went wrong. perhaps you need to login?')))
        sys.exit(-1)
