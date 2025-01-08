import github3
from typing import List, Tuple
from fastapi import HTTPException
from github3.repos import Repository

from app.core.config import settings
from app.core.logger import logger


class GitHubClient:
    def __init__(self):
        self.token = settings.GITHUB_TOKEN
        self.client = github3.login(token=self.token)

    def get_repo_files(self, repo_url: str) -> List[dict]:
        def fetch_files(directory: str) -> List[dict]:
            file_list = []
            for content in repository.directory_contents(directory):
                if content[1].type == "file":
                    if not is_file_allowed(content[1].name):
                        continue

                    file_list.append(
                        {
                            "name": content[1].name,
                            "path": content[1].path,
                        }
                    )
                elif content[1].type == "dir":
                    file_list.extend(fetch_files(content[1].path))
            return file_list

        def is_file_allowed(file_name: str) -> bool:
            excluded_extensions = {".lock", ".log", ".tmp"}
            if any(file_name.endswith(ext) for ext in excluded_extensions):
                return False
            return True

        owner, repo_name = self._parse_repo_url(repo_url)
        repository: Repository = self.client.repository(owner, repo_name)

        if not repository:
            logger.info(f"Repository {owner}/{repo_name} not found or access denied.")
            raise HTTPException(
                status_code=404,
                detail=f"Repository {owner}/{repo_name} not found or access denied.",
            )

        files = fetch_files("/")

        for file in files:
            try:
                file["content"] = repository.file_contents(file["path"]).decoded.decode(
                    "utf-8"
                )
            except Exception as e:
                file["content"] = None
                logger.info(f"Error retrieving content for file {file['path']}: {e}")
                raise HTTPException(
                    status_code=422,
                    detail=f"Error retrieving content for file {file['path']}: {e}",
                )

        return files

    def _parse_repo_url(self, repo_url: str) -> Tuple[str, str]:
        parts = repo_url.rstrip("/").split("/")
        if len(parts) < 2:
            raise HTTPException(status_code=422, detail="Invalid GitHub repository URL")
        return parts[-2], parts[-1]
