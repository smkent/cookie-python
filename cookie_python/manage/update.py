import os
from argparse import Namespace
from pathlib import Path
from typing import Optional

from .repo import RepoSandbox


def update_cruft(repo: RepoSandbox) -> Optional[str]:
    before_ref = repo.cruft_attr("commit")
    repo.run(["poetry", "env", "remove", "--all"], check=False)
    repo.run(["poetry", "env", "use", "/usr/bin/python3"])
    repo.run(["poetry", "install"])
    repo.run(["poetry", "run", "cruft", "update", "-y"])
    after_ref = repo.cruft_attr("commit")
    if before_ref == after_ref:
        return None
    for try_count in range(1):
        rej_files = [
            fn.strip()
            for fn in repo.run(
                ["find", ".", "-iname", "*.rej"],
                capture_output=True,
                check=True,
            )
            .stdout.decode()
            .splitlines()
        ]
        conflicts = any(
            line.startswith("U")
            for line in repo.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                check=True,
            )
            .stdout.decode()
            .splitlines()
        )
        if rej_files or conflicts:
            if try_count == 0:
                print(f">>> Conflicts found: {rej_files}")
                print("Resolve conflicts and exit shell to continue")
                repo.shell()
                continue
            raise Exception(f"Unresolved conflicts: {rej_files}")

    cruft_repo = repo.cruft_attr("template")
    range_prefix = None
    if cruft_repo.startswith("https://github.com"):
        range_prefix = f"{cruft_repo}/compare/"
    if Path(cruft_repo).is_dir():
        template_repo_path = Path(cruft_repo)
    else:
        template_repo_path = repo.tempdir / "cookie_repo"
        repo.run(
            ["git", "clone", cruft_repo, template_repo_path], cwd=repo.tempdir
        )
    compare_cmd = [
        "git",
        "log",
        "--oneline",
        "--graph",
        f"{before_ref}...{after_ref}",
    ]
    graph_output = repo.run(
        compare_cmd, cwd=template_repo_path, capture_output=True, check=True
    ).stdout.decode()
    return (
        "Applied updates from upstream project template commits:\n\n"
        f"{range_prefix or ''}{before_ref}...{after_ref}\n\n"
        f"```\n{graph_output.strip()}\n```\n\n"
    )


def update_dependencies(repo: RepoSandbox) -> Optional[str]:
    repo.run(["poetry", "run", "pre-commit", "autoupdate"])
    updates = repo.run(
        ["poetry", "update", "--no-cache"], capture_output=True
    ).stdout.decode("utf-8")
    print(updates)
    try:
        while (
            not updates.splitlines()[0]
            .lower()
            .startswith("package operations")
        ):
            updates = os.linesep.join(updates.splitlines()[1:])
    except IndexError:
        print("No updates in output detected")
        return None
    update_lines = [u.strip().replace("•", "-") for u in updates.splitlines()]
    if len(update_lines) < 3:
        print("No updates in output detected")
        return None
    return (
        "Updated project dependencies via `poetry update`:"
        + os.linesep * 2
        + os.linesep.join(update_lines)
    )


def update_action(args: Namespace) -> None:
    for repo_url in args.repo:
        with RepoSandbox(repo_url, args.dry_run) as repo:
            actions = []
            msg_body = ""
            cruft_msg = update_cruft(repo)
            if cruft_msg:
                msg_body += cruft_msg
                actions.append("project template cruft")
            deps_msg = update_dependencies(repo)
            if deps_msg:
                msg_body += deps_msg
                actions.append("dependencies")
            if not msg_body:
                return None
            message = f"Update {', '.join(actions)}\n\n{msg_body}"
            repo.commit_changes(message)
            repo.open_pr(message)
