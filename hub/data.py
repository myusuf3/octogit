import os
import sqlite3


HUB_CONFIG_DIR = os.path.expander('~/.config/hub')

def createdb_dir():
    os.mkdir(HUB_CONFIG_DIR)

def createdb():
    :

