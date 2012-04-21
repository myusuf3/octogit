"""
octogit

This file contains stuff for github api
"""

import os
import sys
import shlex
import subprocess

import requests
import simplejson
from git import Repo
from clint.textui import colored, puts, columns

from .config import get_username, get_password


ISSUES_ENDPOINT = 'https://api.github.com/repos/%s/%s/issues'
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
    push_master = 'git push -u origin master'
    args = shlex.split(push_master)
    commit = subprocess.Popen(args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
    stdout = commit.communicate()


def create_octogit_readme():
    filename = 'README.rst'
    FILE = open(filename, "w")
    FILE.write("""========
Octogit
========


This repository has been created with Octogit.


.. image:: http://myusuf3.github.com/octogit/assets/img/readme_image.png

Author
======
Mahdi Yusuf (@myusuf3)
""")
    FILE.close()


def git_add_remote(username, repo_name):
    git_remote = "git remote add origin git@github.com:%s/%s.git" % (username, repo_name)
    args = shlex.split(git_remote)
    commit = subprocess.Popen(args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)


def git_initial_commit():
    git_commit = "git commit -am 'this repository now with more tentacles care of octogit'"
    args = shlex.split(git_commit)

    commit = subprocess.Popen(args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
    stdout = commit.communicate()


def git_add():
    git_add  = "git add README.rst"
    args = shlex.split(git_add)
    commit = subprocess.Popen(args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
    stdout = commit.communicate()



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
        puts('{0}. {1}'.format(colored.blue('octogit'),
            colored.green('this is your moment of glory; Be a hero.')))


def get_number_issues(content):
    count = 0
    for issue in content:
        if issue['pull_request']['html_url'] != None:
            pass
        else:
            count +=1
    return count

def close_issue(user, repo, number):
    if get_username() == '' or get_password() == '':
        puts('{0}. {1}'.format(colored.blue('octogit'),
            colored.red('in order to create a repository, you need to login.')))
        sys.exit(-1)
    update_issue = UPDATE_ISSUE % (user, repo, number)
    post_dict = {'state': 'close'}
    username = get_username()
    password = get_password()
    r = requests.post(update_issue, auth=(username, password), data=simplejson.dumps(post_dict))
    if r.status_code == 200:
        puts('{0}.'.format(colored.red('closed')))
    else:
        puts('{0}. {1}'.format(colored.blue('octogit'),
            colored.red("You either aren't allowed to close repository or you need to login in dummy.")))
        sys.exit(-1)


def create_repository(project_name, description):
    if get_username() == '' or get_password() == '':
        puts('{0}. {1}'.format(colored.blue('octogit'),
            colored.red('in order to create a repository, you need to login.')))
        sys.exit(-1)

    post_dict = {'name': project_name, 'description': description, 'homepage': '', 'private': False, 'has_issues': True, 'has_wiki': True, 'has_downloads': True}
    username = get_username()
    password = get_password()
    re = requests.post('https://api.github.com/user/repos', auth=(username, password), data=simplejson.dumps(post_dict))
    if re.status_code == 201:
        create_local_repo(username, project_name)
    elif simplejson.loads(re.content)['errors'][0]['message'] == 'name already exists on this account':
        puts('{0}. {1}'.format(colored.blue('octogit'),
            colored.red('repository named this already exists on github')))
    else:
        puts('{0}. {1}'.format(colored.blue('octogit'),
            colored.red('in order to create a repository, you need to login.')))
        sys.exit(-1)


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
        puts('{0}. {1}'.format(colored.blue('octogit'),
            colored.red('You need to be inside a valid git repository.')))
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

    issue = simplejson.loads(connect.content)
    width = [[colored.yellow('#'+str(issue['number'])), 5],]
    width.append([colored.red('('+ issue['user']['login']+')'), 15])
    puts(columns(*width))
    description = description_clean(issue['body'])
    puts(description)


def get_issues(user, repo):
    url = ISSUES_ENDPOINT % (user, repo)
    github_issues_url = ISSUES_PAGE %  (user, repo)

    if valid_credentials():
        connect = requests.get(url, auth=(get_username(), get_password()))
    else:
        connect = requests.get(url)

    json_data = simplejson.loads(connect.content)

    try:
        json_data['message']
        puts('{0}. {1}'.format(colored.blue('octogit'),
            colored.red('Do you even have a Github account? Bad Credentials')))
        return
    except:
        pass
    if len(json_data) == 0 :
        puts('{0}. {1}'.format(colored.blue('octogit'),
            colored.cyan('Looks like you are perfect welcome to the club.')))
        return
    get_number_issues(json_data)
    puts('link. {0} \n'.format(colored.green(github_issues_url)))
    puts('listing all {0} issues.'.format(colored.red(get_number_issues(json_data))))
    for issue in json_data:
        #skip pull requests
        if issue['pull_request']['html_url'] != None:
            continue
        width = [[colored.yellow('#'+str(issue['number'])), 5],]
        width.append(['{0}'.format(issue['title']), 70])
        width.append([colored.red('('+ issue['user']['login']+')'), None])
        puts(columns(*width))
