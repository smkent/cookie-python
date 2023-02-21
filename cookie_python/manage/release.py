from argparse import Namespace

import semver

from .repo import RepoSandbox


def release_patch_version(repo: RepoSandbox) -> None:
    releases = (
        repo.run(
            ["gh", "release", "list"],
            capture_output=True,
            check=True,
        )
        .stdout.decode("utf-8")
        .splitlines()
    )
    latest_tag = None
    for line in releases:
        tag, status, *_ = line.split()
        if status.lower() == "latest":
            latest_tag = tag
            break
    if not latest_tag:
        repo.logger.warning("Unable to find latest version")
        return None
    check_refs = ["origin/main", latest_tag]
    refs = []
    for ref in check_refs:
        refs.append(
            repo.run(["git", "rev-parse", ref], capture_output=True)
            .stdout.decode("utf-8")
            .strip()
        )
    if len(refs) == len(check_refs) and len(set(refs)) == 1:
        repo.logger.info(f"No new changes since latest release {latest_tag}")
        return None
    sv = semver.VersionInfo.parse(latest_tag.lstrip("v"))
    next_patch_ver = sv.bump_patch()
    new_tag = f"v{next_patch_ver}"
    if repo.dry_run:
        repo.logger.success(f"Would release new version {new_tag}")
        return None
    repo.run(["gh", "release", "create", new_tag, "--generate-notes"])
    repo.logger.success(f"Releasing new version {new_tag}")
    return None


def release_action(args: Namespace) -> None:
    for repo_url in args.repo:
        with RepoSandbox(repo_url, args.dry_run) as repo:
            release_patch_version(repo)
