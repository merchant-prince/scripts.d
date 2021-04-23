#!/usr/bin/env python3

from argparse import ArgumentParser, Namespace
from subprocess import run

if __name__ == '__main__':
    main_parser: ArgumentParser = ArgumentParser(
        prog='upgrade',
        description='A script to upgrade the system, and its packages.',
        allow_abbrev=False
    )

    all_subparser: ArgumentParser = main_parser.add_subparsers(
        title='Action',
        description='The action to take.',
        dest='action',
        required=True
    ).add_parser(
        'all',
        description='Upgrade the system.',
        add_help=True,
        allow_abbrev=False
    )

    all_subparser.add_argument(
        '--refresh-mirrors',
        action='store_true',
        help="Refresh pacman's mirrors."
    )

    arguments: Namespace = main_parser.parse_args()

    if arguments.action == 'all':
        print('Starting upgrade...')

        if arguments.refresh_mirrors:
            print("Refreshing pacman's mirrors...")
            run(('sudo', 'pacman-mirrors', '-f'), check=True)

        print("Upgrading pacman packages...")
        run(('sudo', 'pacman', '-Syyu'), check=True)

        print("Upgrading AUR packages...")
        run(('pacaur', '-Syuua'), check=True)

        print('Upgrade complete.')
