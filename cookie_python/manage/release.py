from argparse import Namespace

from .repo import RepoSandbox


def release_action(args: Namespace) -> None:
    for repo_url in args.repo:
        with RepoSandbox(repo_url, args.dry_run) as repo:
            print(repo)
