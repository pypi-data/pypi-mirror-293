# github-utility

A simple Python package for interacting with the GitHub API.

## Installation

```bash
pip install github-utility
```

## Usage
### Script Based
```python
from github_utils import GitHubAPI

# Set your GitHub access token
access_token = "YOUR_ACCESS_TOKEN"

github_api = GitHubAPI(access_token)

# Get user information
user_data = github_api.get_user("shivampatil5606")
print(user_data)

# Create a new issue
issue_data = github_api.create_issue(
    owner="owner",
    repo="repo",
    title="Test Issue",
    body="This is a test issue."
)
print(issue_data)
```

### CLI Based
```bash
export GITHUB_ACCESS_TOKEN="YOUR_ACCESS_TOKEN"

# To get the user details
github-utility get-user --username <username>

# To create an issue on GitHub
github-utility create-issue -o <repo-owner> -r <repo-name> -t <issue-title> -b <issue-body>

```
