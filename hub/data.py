#!/usr/bin/python


import os
import sqlite3

from clint import args
from clint.textui import colored, puts, indent


HUB_CONFIG_DIR = os.path.expander('~/.config/hub')
HUB_DB = os.path.expander('~/.config/hub/hub.db')
HUB_DB_CREATED = os.path.exists(HUB_DB)
HUB_SCHEMA = os.path.expander('../schema/hub_schema.sql')

def createdb_dir():
    os.mkdir(HUB_CONFIG_DIR)

def createdb():
    if HUB_DB_CREATED:
        puts(colored.red('User already authenticated!'))
        puts(colored.cyan('Run <hub login> to authenticate as new user'))
    else:
        hub_connect = sqlite3.connect(HUB_DB) 
        with open(HUB_SCHEMA, 'rt') as f:
            hub_schema = f.read()
        hub_connect.executescript(hub_schema)
        hub_connect.close()

def login_data(username, password):
    hub_connect = sqlite3.connect(HUB_DB)
    hub_connect.execute('INSERT INTO hub VALUES(?, ?)', (username, password))
    hub_connect.commit()
    hub_connect.close()




