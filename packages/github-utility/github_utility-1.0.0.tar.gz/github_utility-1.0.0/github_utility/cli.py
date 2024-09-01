import argparse
import importlib.metadata
import os

from .github import GitHubAPI


def main():
    # Get the version from the metadata.
    #   For running slash tests if jira-ticket-automation package not found set default to 1.0.0.
    try:
        __version__ = importlib.metadata.version("github-utility")
    except importlib.metadata.PackageNotFoundError:
        __version__ = "1.0.0"  # Set a default version

    parser = argparse.ArgumentParser(description="GitHub Utility CLI")
    parser.add_argument("-v", "--version", action="version", version=__version__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Get User Command
    get_user_parser = subparsers.add_parser("get-user", help="Utility to view user details")
    get_user_parser.add_argument(
        "-u","--username",
        help="GitHub username",
        type=str,
        required=True,
    )

    # Create Issue Command
    create_issue_parser = subparsers.add_parser("create-issue", help="Utility to create issues on Github")
    create_issue_parser.add_argument(
        "-o", "--owner",
        help="Repository owner",
        type=str,
        required=True,
    )
    create_issue_parser.add_argument(
        "-r", "--repo",
        help="Repository name",
        type=str,
        required=True,
    )
    create_issue_parser.add_argument(
        "-t", "--title",
        help="Issue title",
        type=str,
        required=True,
    )
    create_issue_parser.add_argument(
        "-b", "--body",
        help="Issue body",
        type=str,
        required=True,
    )

    args = parser.parse_args()

    # Get access token from environment variable
    access_token = os.getenv("GITHUB_ACCESS_TOKEN")
    if not access_token:
        print("Error: GITHUB_ACCESS_TOKEN environment variable not set.")
        exit(1)

    github_api = GitHubAPI(access_token)

    if args.command == "get-user":
        user_data = github_api.get_user(args.username)
        print(user_data)
    elif args.command == "create-issue":
        issue_data = github_api.create_issue(args.owner, args.repo, args.title, args.body)
        print(issue_data)

if __name__ == "__main__":
    main()
