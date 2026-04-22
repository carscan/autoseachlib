"""
Command-line interface for AutoSeachLib.

Usage:
    autoseachlib hello          Print hello world greeting
    autoseachlib add "a" "b"    Concatenate two strings
    autoseachlib --version      Show package version
"""

import argparse
import sys

from autoseachlib import __version__
from autoseachlib.core import hello_world, add_strings


def build_parser() -> argparse.ArgumentParser:
    """Build and return the argument parser."""
    parser = argparse.ArgumentParser(
        prog="autoseachlib",
        description="AutoSeachLib — Automated Research Library for CarScan.ai",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "examples:\n"
            "  autoseachlib hello\n"
            '  autoseachlib add "Hello, " "World!"\n'
            "  autoseachlib --version\n"
        ),
    )
    parser.add_argument(
        "--version", "-V",
        action="version",
        version=f"autoseachlib {__version__}",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- hello command ---
    subparsers.add_parser(
        "hello",
        help="Print hello world greeting",
    )

    # --- add command ---
    add_parser = subparsers.add_parser(
        "add",
        help="Concatenate two strings",
    )
    add_parser.add_argument("a", type=str, help="First string")
    add_parser.add_argument("b", type=str, help="Second string")

    # --- download command ---
    download_parser = subparsers.add_parser(
        "download",
        help="Download a file from S3",
    )
    download_parser.add_argument("bucket", help="S3 bucket name")
    download_parser.add_argument("key", help="S3 key (path)")
    download_parser.add_argument("local_path", help="Local destination path")
    download_parser.add_argument("--access-key", help="AWS access key")
    download_parser.add_argument("--secret-key", help="AWS secret key")
    download_parser.add_argument("--region", help="AWS region")

    return parser


def main(argv: list[str] | None = None) -> int:
    """CLI entry point.

    Args:
        argv: Command-line arguments (defaults to sys.argv[1:]).

    Returns:
        int: Exit code (0 for success, 1 for error).
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 1

    if args.command == "hello":
        hello_world()
        return 0

    if args.command == "add":
        result = add_strings(args.a, args.b)
        print(result)
        return 0

    if args.command == "download":
        success = download_image(
            bucket=args.bucket,
            key=args.key,
            local_path=args.local_path,
            access_key=args.access_key,
            secret_key=args.secret_key,
            region_name=args.region
        )
        return 0 if success else 1

    return 1


if __name__ == "__main__":
    sys.exit(main())
