import argparse
from zipignore.core import zip_project

def main():
    parser = argparse.ArgumentParser(
        description="Zip your project folder excluding files with .zipignore rules"
    )

    parser.add_argument(
        "--base",
        type=str,
        default=".",
        help="Base folder to zip (default: current directory)"
    )

    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Custom zip filename (optional, otherwise auto-generated)"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List files that would be zipped, but do not create the zip file"
    )

    args = parser.parse_args()

    zip_project(base_folder=args.base, zip_name=args.output, dry_run=args.dry_run)
