from .types import (
    AttributeValue,
)
import argparse as _argparse
from decimal import (
    Decimal,
)
import os as _os
from typing import (
    cast,
    NamedTuple,
)


class Args(NamedTuple):
    test_path: str
    cov_path: str | None
    scope: str | None


def get_args() -> Args:
    parser = _argparse.ArgumentParser(
        prog="fluidattacks_core.testing",
        description=(
            "🏹 Python package for unit and integration testing through "
            "Fluid Attacks projects 🏹"
        ),
    )

    parser.add_argument(
        "--target",
        metavar="TARGET",
        type=str,
        default="",
        help="Folder to start the tests. Default is current folder.",
    )

    parser.add_argument(
        "--cov",
        metavar="COV",
        type=str,
        default="src",
        help="The source code for coverage report. Default is src.",
    )

    parser.add_argument(
        "--no-cov",
        action="store_true",
        help="Do not generate coverage report.",
    )

    parser.add_argument(
        "--test-folder",
        metavar="TEST_FOLDER",
        type=str,
        default="test",
        help="Folder with tests inside the target. Default is test.",
        nargs="?",
    )

    parser.add_argument(
        "--scope",
        metavar="SCOPE",
        type=str,
        help="Type and module to test.",
    )
    args = parser.parse_args()

    target = cast(str, args.target if args.target else _os.getcwd())
    scope = cast(str, args.scope if args.scope else None)
    tests = cast(str, args.test_folder)

    test_path = _os.path.join(target, tests)
    if not _os.path.isdir(test_path):
        raise FileExistsError(f"Test folder not found: {test_path}")

    unit_tests_path = _os.path.join(test_path, "unit/src")
    if not _os.path.isdir(unit_tests_path):
        raise FileExistsError(f"Unit test folder not found: {tests}/unit/src")

    cov_path: str | None = (
        None if args.no_cov else _os.path.join(target, args.cov)
    )
    if cov_path and not _os.path.isdir(cov_path):
        raise FileExistsError(f"Source folder not found: {cov_path}")

    return Args(
        test_path=unit_tests_path,
        cov_path=cov_path,
        scope=scope,
    )


def _cast_primitive(
    value: str | bool | int | float | Decimal,
) -> AttributeValue:
    if isinstance(value, (str)):
        return {"S": str(value)}
    if isinstance(value, (bool)):
        return {"BOOL": value}
    return {"N": str(value)}


def _cast_objects(value: list | dict) -> AttributeValue:
    if isinstance(value, list):
        return {"L": [cast_to_dynamodb(v) for v in value]}
    return {"M": {key: cast_to_dynamodb(val) for key, val in value.items()}}


def cast_to_dynamodb(
    value: str | bool | int | float | dict | Decimal | None,
) -> AttributeValue:
    """Format vulnerabilities to DynamoDB structure.

    Returns:
        AttributeValue: Vulnerability formatted to DynamoDB types.
    """
    if isinstance(value, (str, bool, int, float, Decimal)):
        return _cast_primitive(value)
    if isinstance(value, (dict, list)):
        return _cast_objects(value)
    return {"NULL": True}
