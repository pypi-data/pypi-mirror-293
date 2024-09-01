import requests


class GitHubAPI:
    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {self.access_token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def get_user(self, username):
        """Fetches user information from the GitHub API.

        Args:
            username: The GitHub username.

        Returns:
            A dictionary containing user information.
        """
        url = f"{self.base_url}/users/{username}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()

    def create_issue(self, owner, repo, title, body):
        """Creates a new issue on a GitHub repository.

        Args:
            owner: The owner of the repository.
            repo: The name of the repository.
            title: The title of the issue.
            body: The body of the issue.

        Returns:
            A dictionary containing the created issue information.
        """
        url = f"{self.base_url}/repos/{owner}/{repo}/issues"
        data = {"title": title, "body": body}
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()
