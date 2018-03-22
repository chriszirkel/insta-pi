import argparse
import sys
import threading

from instapi import viewer
from instapi import parser


def continuous_parse():
    viewer.after(86400*1000, continuous_parse)
    parser.parse()


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='Process some integers.')
    arg_parser.add_argument('-u', '--username', required=True, help='instagram username')
    arg_parser.add_argument('-p', '--password', required=True, help='instagram password')
    arg_parser.add_argument('-d', '--directory', required=True, help='directory to store images')
    arg_parser.add_argument('-i', '--interval', required=False, default=60, help='shuffle image interval in seconds')
    arg_parser.add_argument('-b', '--browser', required=False, choices=['Firefox', 'Chrome', 'PhantomJS'], default='PhantomJS', help='browser to parse instagram')
    args = arg_parser.parse_args()

    if not args.username or not args.password or not args.directory:
        print('username or password or directory is empty')
        sys.exit(0)

    parser = parser.Parser(url='https://www.instagram.com', dir=args.directory, username=args.username, password=args.password, browser=args.browser)
    viewer = viewer.Viewer(dir=args.directory, interval=args.interval)

    continuous_parse()
    viewer.view()

