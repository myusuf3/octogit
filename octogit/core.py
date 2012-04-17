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

def push_to_master():
    push_master = 'git push -u origin master'
    args = shlex.split(push_master)
    commit = subprocess.Popen(args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
    stdout = commit.communicate()
    print stdout

def create_octogit_readme():
    filename = 'octogit.txt'
    FILE = open(filename, "w")
    FILE.write('This repository has been created by Octogit')
    FILE.close()

def git_add_remote(username, repo_name):
    git_remote = "git remote add origin git@github.com:%s/%s.git" % (username, repo_name)
    args = shlex.split(git_remote)
    commit = subprocess.Popen(args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
    stdout = commit.communicate()
    print stdout

def git_initial_commit():
    git_commit = "git commit -am 'this repository now with more tentacles care of octogit'"
    args = shlex.split(git_commit)

    commit = subprocess.Popen(args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
    stdout = commit.communicate()
    print stdout

def git_add():
    git_add  = "git add octogit.txt"
    args = shlex.split(git_add)
    commit = subprocess.Popen(args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
    stdout = commit.communicate()
    print stdout

def create_local_repo(username, repo_name):
    import pdb; pdb.set_trace()
    # mkdir repo_name
    
    os.makedirs('/'.join([os.getcwd(), repo_name]))
    # cd repo_name
    os.chdir('/'.join([os.getcwd(), repo_name]))
    #git init
    repository = Repo.init(os.getcwd())
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

def create_repository():
    import pdb; pdb.set_trace()
    post_dict = {'name': 'Hello-World', 'description': 'This is your first repo','homepage': 'https://github.com', 'private': False, 'has_issues': True, 'has_wiki': True,'has_downloads': True}
    r = requests.post('https://api.github.com/user/repos', auth=('myusuf3', ''), data=simplejson.dumps(post_dict))
    if r.status_code == 201:
        create_local_repo('myusuf3', 'Hello-World')
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
