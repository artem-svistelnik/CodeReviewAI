from pydantic import AnyUrl

from schemas.base import BaseSchemaModel
from enum import Enum


class CandidateLevel(str, Enum):
    JUNIOR = "JUNIOR"
    MIDDLE = "MIDDLE"
    SENIOR = "SENIOR"


class ReviewRequest(BaseSchemaModel):
    assignment_description: str
    github_repo_url: AnyUrl
    candidate_level: CandidateLevel
