# -*- coding: utf-8 -*-
import argparse
import getpass
import os
import sys

from termcolor import cprint
from gitsync.providers.github_provider import GithubProvider
from gitsync.providers.tuleap_provider import TuleapProvider

from gitsync.providers.file_provider import FileProvider
from gitsync.synchgit import GitSync


def parse_args():
    parser = argparse.ArgumentParser(
        description='Git sync tool'
    )

    parser.add_argument(
        '--provider',
        dest='repository_provider',
        default="file",
        help='git-sync provider: github, tuleap, file (default)'
    )

    parser.add_argument(
        '--workspace',
        dest='workspace',
        default="/tmp",
        help='Working directory'
    )

    parser.add_argument(
        '--github.username',
        dest='github_username',
        help='Github username'
    )

    parser.add_argument(
        '--tuleap.host',
        dest='tuleap_host',
        help='Tuleap hostname'
    )

    parser.add_argument(
        '--tuleap.username',
        dest='tuleap_username',
        help='Tuleap username'
    )

    parser.add_argument(
        '--tuleap.project',
        dest='tuleap_project',
        help='Tuleap project'
    )
    args = parser.parse_args()
    return args


def main():
    try:
        args = parse_args()
        repository_provider = FileProvider()

        if args.repository_provider == 'github':
            if args.github_username:
                password = getpass.getpass('Your Github password:')
                repository_provider = GithubProvider(args.github_username, password, args.workspace)
            else:
                raise ValueError("Unkown github username")

        if args.repository_provider == 'tuleap':
            if args.tuleap_username:
                password = getpass.getpass('Your Tuleap password:')
                repository_provider = TuleapProvider(args.tuleap_host, args.tuleap_username,
                                                     password, args.tuleap_project, args.workspace)
            else:
                raise ValueError("Unkown tuleap username")

        GitSync(os.getcwd(), repository_provider).sync_all()

    except KeyboardInterrupt:
        cprint("... terminating git-sync", "green")
        sys.exit(130)
    except Exception as e:
        cprint(text=str(e), color='red', attrs=['bold'])
        sys.exit(1)


if __name__ == "__main__":
    main()
