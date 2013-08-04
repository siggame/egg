#!/usr/bin/env python

from sh import git, ErrorReturnCode
import sys
import grabber
import maker

try:
    #rename raw_input to input in Python 2
    input = raw_input
except:
    #if raw_input doesn't exist, we're on 3 and fine
    pass

def show_help():
    print('Usage: %s [command]')
    print('Commands:')
    print('init\t\t-- initialize the repository')
    print('update\t\t-- update after component of data.yaml change')

def init():
    url = input('Remote repository url: ')
    git.remote('set-url', 'origin', url)
    git.push('-u', 'origin', 'master')
    git.checkout('-b', 'run-codegen')
    git.push('-u', 'origin', 'run-codegen')
    git.checkout('master')

def update():
    try:
        git.show('master:data.yaml', _tty_out=False)
    except ErrorReturnCode:
        print('Error: data.yaml not committed to master')
        sys.exit(1)
    grabber.grab_components()
    git.checkout('run-codegen')
    git.checkout('master', '--', 'data.yaml')

    maker.make_all()
    git.add('-A')
    git.commit(message = 'codegen rerun')
    git.checkout('master')
    git.merge('run-codegen', '--no-commit')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        show_help()
    elif sys.argv[1] == 'init':
        init()
    elif sys.argv[1] == 'update':
        update()
    else:
        show_help()

