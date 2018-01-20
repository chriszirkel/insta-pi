import argparse
import sys
import threading

from instapi import viewer
from instapi import parser


def view():
    viewer.view()


def parse():
    parser.parse()
    threading.Timer(3600, parse).start()


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='Process some integers.')
    arg_parser.add_argument('-u', '--username', required=True, help='instagram username')
    arg_parser.add_argument('-p', '--password', required=True, help='instagram password')
    args = arg_parser.parse_args()

    if not args.username or not args.password:
        print('username or password is empty')
        sys.exit(0)

    parser = parser.Parser(url='https://www.instagram.com', dir='images', username=args.username, password=args.password)
    viewer = viewer.Viewer('images')

    parse()
    view()

