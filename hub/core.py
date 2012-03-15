#!/usr/bin/env python
"""
hub

this file contains github api stuff
"""


import urllib

import simplejson
from clint.textui import colored, puts, indent


ISSUES_ENDPOINT = 'https://api.github.com/repos/%s/%s/issues'

def get_issues(user, repo):
    url = ISSUES_ENDPOINT % (user, repo)
    connect = urllib.urlopen(url)
    json_data = simplejson.load(connect)
    puts('Issues: ')
    for i in json_data:
        issue_info = '    '.join((
                '{0}'.format(colored.red(i['number'])),
                '{0}'.format(colored.cyan(i['user']['login'])),
                '{0}'.format(i['title'])
                ))
        puts(issue_info)

if __name__ == '__main__':
    exit(get_issues('github','hubot'))
