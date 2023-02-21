from argparse import Namespace

from .repo import RepoSandbox


def update_action(args: Namespace) -> None:
    for repo in args.repo:
        with RepoSandbox(repo):
            pass
