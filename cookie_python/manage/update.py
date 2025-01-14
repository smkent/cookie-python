import os
from pathlib import Path
from typing import Optional

from .repo import RepoSandbox


def reset_cruft_json(repo: RepoSandbox) -> None:
    repo.run(
        ["git", "checkout", "--", ".cruft.json"],
        capture_output=True,
        check=False,
    )


def update_cruft(repo: RepoSandbox) -> Optional[str]:
    before_ref = repo.cruft_attr("commit")
    repo.run(["poetry", "env", "remove", "--all"], check=False)
    repo.run(["poetry", "env", "use", "/usr/bin/python3"])
    repo.run(["poetry", "install"])
    repo.run(["poetry", "run", "pip", "install", "toml"])
    repo.run(["poetry", "run", "cruft", "update", "-y"])
    after_ref = repo.cruft_attr("commit")
    if before_ref == after_ref:
        return None
    git_status = (
        repo.run(
            ["git", "status", "--porcelain", "--", ":!.cruft.json"],
            capture_output=True,
            check=True,
        )
        .stdout.decode()
        .strip()
        .splitlines()
    )
    if not git_status:
        # Skip updates with no template changes
        reset_cruft_json(repo)
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
        conflicts = any(line.startswith("U") for line in git_status)
        if rej_files or conflicts:
            if try_count == 0:
                repo.logger.error(f"Conflicts found: {rej_files}")
                repo.logger.error(
                    "Resolve conflicts and exit shell to continue"
                )
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


def update_action(repo: RepoSandbox) -> None:
    repo.logger.info("Starting update")
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
        repo.logger.info("Already up to date")
        return
    actions_str = ", ".join(actions)
    message = f"Update {actions_str}\n\n{msg_body}"
    repo.logger.info(f"Updated {actions_str}")
    repo.commit_changes(message)
    repo.open_pr(message)
    repo.run(["poetry", "env", "remove", "--all"], check=False)
