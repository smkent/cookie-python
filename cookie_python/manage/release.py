from argparse import Namespace

import semver

from .repo import RepoSandbox


def release_patch_version(repo: RepoSandbox) -> None:
    if not repo.latest_release:
        repo.logger.warning("Unable to find latest release version")
        return
    check_refs = ["origin/main", repo.latest_release]
    refs = []
    for ref in check_refs:
        refs.append(
            repo.run(["git", "rev-parse", ref], capture_output=True)
            .stdout.decode("utf-8")
            .strip()
        )
    if len(refs) == len(check_refs) and len(set(refs)) == 1:
        repo.logger.info(
            f"No new changes since latest release {repo.latest_release}"
        )
        return
    sv = semver.VersionInfo.parse(repo.latest_release.lstrip("v"))
    next_patch_ver = sv.bump_patch()
    new_tag = f"v{next_patch_ver}"
    if repo.dry_run:
        repo.logger.success(f"Would release new version {new_tag}")
        return
    repo.create_release(new_tag)
    repo.logger.success(f"Released new version {new_tag}")


def release_action(args: Namespace) -> None:
    for repo_url in args.repo:
        with RepoSandbox(repo_url, args.dry_run) as repo:
            release_patch_version(repo)
