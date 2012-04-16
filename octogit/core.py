"""
octogit

This file contains stuff for github api
"""

import os
import sys
import shlex
import urllib
import subprocess

import requests
import simplejson
from clint.textui import colored, puts, indent, columns
from git import Repo


ISSUES_ENDPOINT = 'https://api.github.com/repos/%s/%s/issues'
SINGLE_ISSUE_ENDPOINT = 'https://api.github.com/repos/%s/%s/issues/%s'

def create_octogit_readme():
    pass


def create_local_repo(repo_name):
    # mkdir repo_name
    repo_locaton = '/'.join([os.getcwd(), repo_name])
    os.makedirs(repo_location)
    # cd repo_name
    os.chdir(repo_location)



def create_repository():
    import pdb; pdb.set_trace()
    post_dict = {'name': 'Hello-World', 'description': 'This is your first repo','homepage': 'https://github.com', 'private': False, 'has_issues': True, 'has_wiki': True,'has_downloads': True}
    r = requests.post('https://api.github.com/user/repos', auth=('myusuf3', ''), data=simplejson.dumps(post_dict))
    if r.status_code == 201:
        create_local_repo('Hello-World')
    print r.text

def get_repository():
    get_top_level_repo = 'git rev-parse --show-toplevel'
    args = shlex.split(get_top_level_repo)

    work_path = subprocess.Popen(args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)

    stdout, sterr = work_path.communicate()

    if stdout:
        return Repo(stdout.rstrip('\n'))
    else:
        puts(colored.red('Not a git repository')) 
        sys.exit(0)

def get_single_issue(user, repo, number):
    url = SINGLE_ISSUE_ENDPOINT % (user, repo, number)
    import pdb; pdb.set_trace()
    connect = urllib.urlopen(url)
    json_data = simplejson.load(connect)
    issue_info = '    '.join((
            '{0}'.format(colored.green(json_data['number'])),
            '{0}'.format(colored.red(json_data['user']['login'])),
            '{0}'.format(json_data['title']),
            '{0}'.format(json_data['body'])
            ))
    puts(issue_info)

def get_issues(user, repo):
    url = ISSUES_ENDPOINT % (user, repo)
    print url
    connect = urllib.urlopen(url)
    json_data = simplejson.load(connect)
    try:
        json_data['message']
        puts(colored.cyan('Yay! No issues yet...'))
        return
    except:
        pass
    if len(json_data) == 0 :
        puts(colored.cyan('Yay! No issues yet...'))
        return
    puts('listing all {0} issues.'.format(colored.red(len(json_data))))
    puts('\n')

    for issue in json_data:
        number = str(colored.yellow(issue['number']))
        width = [[number, 10],]
        width.append([colored.yellow(issue['user']['login']), 10])
        width.append(['{0}'.format(issue['title']), 160])
        puts(columns(*width))
