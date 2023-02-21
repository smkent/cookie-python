import contextlib
import os
from functools import cached_property, lru_cache

from github import Github
from github.Repository import Repository


class GithubRepo:
    def __init__(self) -> None:
        self._gh = Github(os.environ["GITHUB_ACCESS_TOKEN"])

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
