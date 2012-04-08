#!/usr/bin/python

import os

from clint import args
from clint.textui import colored, puts, indent

HUB_CONFIG = os.path.expander('~/.config/octogit')


def create_config_directory():
    os.mkdir(HUB_CONFIG)
