#!/usr/bin/env python

from twisted.scripts.twistd import run
from os.path import join, dirname
from sys import argv
import engine


def main():
    argv[1:1] = ['-n', '-y', join(dirname(engine.__file__), 'txapp.py')]
    run()


if __name__ == '__main__':
    main()
