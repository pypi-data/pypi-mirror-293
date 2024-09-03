import argparse
from llm_components.loaders.code_base import map_codebase_to_text
from llm_components.loaders.git_utils import clone_repository
from llm_components.version import __version__
from pathlib import Path
import tempfile

def main():
    parser = argparse.ArgumentParser(description="Map codebase to text")
    parser.add_argument(
        "root_dir_or_repo",
        type=str,
        nargs="?",
        help="Root directory of the codebase or git repository URL",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Display the current version of the package",
    )
    args = parser.parse_args()

    if args.version:
        print(f"llm-components version {__version__}")
        return

    if not args.root_dir_or_repo:
        parser.print_help()
        return

    if args.root_dir_or_repo.startswith(
        "http://"
    ) or args.root_dir_or_repo.startswith("https://"):
        with tempfile.TemporaryDirectory() as temp_dir:
            clone_dir = Path(temp_dir) / "repo"
            clone_repository(args.root_dir_or_repo, clone_dir)
            result = map_codebase_to_text(clone_dir)
    else:
        root_dir = Path(args.root_dir_or_repo)
        result = map_codebase_to_text(root_dir)

    print(result)

if __name__ == "__main__":
    main()
