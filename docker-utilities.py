#!/usr/bin/env python3

from argparse import ArgumentParser, Namespace
from collections import namedtuple
from subprocess import run, PIPE
from types import SimpleNamespace
from typing import Tuple

if __name__ == '__main__':
    parser = namedtuple('Parser', ('main', 'subparser', 'subparsers'))(
        main := ArgumentParser(
            prog='docker-utilities',
            description='A script for high-level docker-management.',
            allow_abbrev=False
        ),
        main.add_subparsers(
            title='Action',
            description='The action to take.',
            dest='action',
            required=True
        ),
        SimpleNamespace()
    )

    # purge
    parser.subparsers.purge = parser.subparser.add_parser(
        'purge',
        description='Purge all docker images, containers, volumes, and networks.',
        add_help=True,
        allow_abbrev=False
    )

    # status
    parser.subparsers.status = parser.subparser.add_parser(
        'status',
        description='Get the status of all docker images, containers, volumes, and networks.',
        add_help=True,
        allow_abbrev=False
    )

    arguments: Namespace = parser.main.parse_args()

    if arguments.action == 'status':
        print('** CONTAINERS **')
        run(('docker', 'container', 'ls', '--all'))
        print()

        print('** VOLUMES **')
        run(('docker', 'volume', 'ls'))
        print()

        print('** IMAGES **')
        run(('docker', 'image', 'ls', '--all'))
        print()

        print('** NETWORKS **')
        run(('docker', 'network', 'ls'))
        print()

    elif arguments.action == 'purge':
        containers: Tuple[str, ...] = tuple(
            container.strip() for container in
            run(
                ('docker', 'container', 'ls', '--all', '--quiet'),
                stdout=PIPE
            ).stdout.decode('utf-8').split()
        )

        print('Stopping all containers...')
        for container in containers:
            run(('docker', 'container', 'stop', container))

        print('Removing all containers...')
        for container in containers:
            run(('docker', 'container', 'rm', '--force', container))

        volumes: Tuple[str, ...] = tuple(
            volume.strip() for volume in
            run(
                ('docker', 'volume', 'ls', '--quiet'),
                stdout=PIPE
            ).stdout.decode('utf-8').split()
        )

        print('Removing all volumes...')
        for volume in volumes:
            run(('docker', 'volume', 'rm', '--force', volume))

        images: Tuple[str, ...] = tuple(
            image.strip() for image in
            run(
                ('docker', 'image', 'ls', '--all', '--quiet'),
                stdout=PIPE
            ).stdout.decode('utf-8').split()
        )

        print('Removing all images...')
        for image in images:
            run(('docker', 'image', 'rm', '--force', image))

        networks: Tuple[str, ...] = tuple(
            network.strip() for network in
            run(
                ('docker', 'network', 'ls', '--quiet'),
                stdout=PIPE
            ).stdout.decode('utf-8').split()
        )

        print('Removing all networks...')
        for network in networks:
            run(('docker', 'network', 'rm', network))
