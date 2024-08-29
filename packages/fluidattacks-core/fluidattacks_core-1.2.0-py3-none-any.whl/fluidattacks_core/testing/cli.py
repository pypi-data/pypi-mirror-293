from .aws.plugins import (
    MotoPlugin,
)
from .plugins import (
    CustomFixturesPlugin,
)
from .utils import (
    get_args,
)
import pytest as _pytest
import sys as _sys


def execute() -> None:
    args = get_args()

    _coverage_args = (
        [
            "--cov",
            f"{args.cov_path}",
            "--cov-branch",
            "--cov-report",
            "term",
            "--no-cov-on-fail",
        ]
        if args.cov_path
        else []
    )
    _scope_args = ["-m", f"{args.scope}"] if args.scope else []
    _pytest_args = [
        *_coverage_args,
        "--disable-warnings",
        "--showlocals",
        "--strict-markers",
        *_scope_args,
        "-rfs",
        "-vvl",
    ]
    _sys.exit(
        _pytest.main(
            [args.test_path, *_pytest_args],
            plugins=[
                CustomFixturesPlugin(),
                MotoPlugin(),
            ],
        )
    )
