from dataclasses import dataclass
from typing import Any, Iterable, List


@dataclass
class ParametrizeParams:
    argnames: Iterable[str]
    argvalues: Iterable[Any]
    ids: Iterable[str]


@dataclass
class ReadmeCase:
    id: str
    argvalues: Iterable[str]


@dataclass
class ReadmeCaseParams:
    id: str
    github_user: str
    enable_coverage: bool
    enable_pypi_publish: bool


class ReadmeCases:
    @classmethod
    def all_cases(
        cls,
    ) -> ParametrizeParams:
        argnames = [
            "github_user",
            "enable_coverage",
            "enable_pypi_publish",
            "expected_content_file",
        ]
        ids: List[str] = []
        argvalues: List[Any] = []
        for case in [
            ReadmeCaseParams(
                id="no_github_user",
                github_user="",
                enable_coverage=False,
                enable_pypi_publish=False,
            ),
            ReadmeCaseParams(
                id="no_github_user_coverage_enabled",
                github_user="",
                enable_coverage=True,
                enable_pypi_publish=False,
            ),
            ReadmeCaseParams(
                id="no_github_user_pypi_enabled",
                github_user="",
                enable_coverage=False,
                enable_pypi_publish=True,
            ),
            ReadmeCaseParams(
                id="github_user_only",
                github_user="ness",
                enable_coverage=False,
                enable_pypi_publish=False,
            ),
            ReadmeCaseParams(
                id="github_user_with_coverage",
                github_user="ness",
                enable_coverage=True,
                enable_pypi_publish=False,
            ),
            ReadmeCaseParams(
                id="github_user_with_pypi",
                github_user="ness",
                enable_coverage=False,
                enable_pypi_publish=True,
            ),
            ReadmeCaseParams(
                id="github_user_with_coverage_and_pypi",
                github_user="ness",
                enable_coverage=True,
                enable_pypi_publish=True,
            ),
        ]:

            ids.append(case.id)
            argvalues.append(
                [
                    case.github_user,
                    case.enable_coverage,
                    case.enable_pypi_publish,
                    f"tests/data/readme-{case.id}.md",
                ]
            )
        return ParametrizeParams(
            argnames=argnames, argvalues=argvalues, ids=ids
        )
