from clients.github import GitHubClient


def test_get_repo_files():
    github_client = GitHubClient()
    files = github_client.get_repo_files(
        "https://github.com/artem-svistelnik/CodeReviewAI"
    )
    assert isinstance(files, list)
    assert "name" in files[0]
    assert "path" in files[0]
