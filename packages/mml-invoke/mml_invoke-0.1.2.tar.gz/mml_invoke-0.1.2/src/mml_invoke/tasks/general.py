from typing import Literal

from invoke import task


@task
def bump_version(
    ctx,
    bump_type: Literal[
        "major", "minor", "patch", "prepatch", "preminor", "premajor", "prerelease"
    ],
) -> None:
    """
    Bump project/program version

    Parameters
    ----------
    ctx:
        Invoke context
    bump_type: Literal
        one of the following:
        "major": 1.0.0 -> 2.0.0
        "minor": 1.0.0 -> 1.1.0
        "patch": 1.0.0 -> 1.0.1
        "prepatch": 1.0.0 -> 1.0.1a
        "preminor": 1.0.0 -> 1.1.0a
        "premajor": 1.0.0 -> 2.0.0a
        "prerelease"
    """
    if bump_type not in [
        "major",
        "minor",
        "patch",
        "prepatch",
        "preminor",
        "premajor",
        "prerelease",
    ]:
        raise ValueError("bump_type must be either 'major' or 'minor' or 'patch'")

    ctx.run(f"poetry version {bump_type}")
