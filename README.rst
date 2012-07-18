========
Octogit
========

.. image:: https://github.com/myusuf3/octogit/raw/gh-pages/assets/img/readme_image.png
   :align: center

A **free** and **open source** interface to github from the command line. Avoid the usual copy and paste when creating repositories, keep up to date on issues, and much more.

--Everybody loves more tentacles.


Installation
============

Installing using pip. ::

    pip install octogit


Using Octogit
==============

Available commands. ::

    octogit login 
    # allows you to store your github authentication data 

    octogit create <reponame> 'description' 
    # lets you create the repository both locally and on github 

    octogit issues 
    # lets you see all the related issues in the current repository 

    octogit issues <number> 
    # lets you see a specific issue with summary 

    octogit issues <number> close 
    # lets you close an issue

    octogit gists delete <number>
    # lets you delete a gist

    octogit gists create <file1> <file2> <fileN> 'description'
    # lets you create a gist with one or more files
    # accepts absolute and relative file paths


Contribute
==========
If you would like to contribute simply fork this project and add yourself to the AUTHORS.txt along with some changes hopefully and submit a pull request.


