import contextlib
import os
from functools import cached_property, lru_cache
from typing import Optional

import github
from github.PullRequest import PullRequest
from github.Repository import Repository


class GithubRepo:
    def __init__(self) -> None:
        self._gh = github.Github(os.environ["GITHUB_API_TOKEN"])

    @cached_property
    def username(self) -> str:
        return self._gh.get_user().login

    @lru_cache  # noqa: B019
    def find_repo(self, search: str) -> Repository:
        if "/" not in search:
            search = f"{self.username}/{search}"
        if "github.com" in search:
            with contextlib.suppress(IndexError):
                search = os.path.splitext(search.split(":")[1])[0]
        return self._gh.get_repo(search)

    def find_pr(
        self, repo: Repository, head: str, base: str = "main"
    ) -> Optional[PullRequest]:
        pulls = [
            pr
            for pr in repo.get_pulls(head=f"{self.username}:{head}", base=base)
        ]
        if not pulls:
            return None
        if len(pulls) > 1:
            raise Exception(f"Multiple PRs found matching {head}")
        return pulls[0]
