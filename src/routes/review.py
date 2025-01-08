import hashlib

from fastapi import APIRouter
from fastapi import Depends

from app.core.dependencies import get_github_client
from app.core.dependencies import get_openai_client
from app.core.dependencies import get_redis_connection
from app.core.logger import logger
from clients.github import GitHubClient
from clients.openai import OpenAIClient
from schemas.review import CandidateLevel
from schemas.review import ReviewRequest

review_router = APIRouter(prefix="/review", tags=["Review"])


@review_router.post("")
async def review(
    review_request: ReviewRequest,
    redis=Depends(get_redis_connection),
    github_client: GitHubClient = Depends(get_github_client),
    openai_client: OpenAIClient = Depends(get_openai_client),
):
    cache_key = hashlib.md5(
        f"{review_request.assignment_description}-{review_request.candidate_level}".encode(
            "utf-8"
        )
    ).hexdigest()

    cached_review = await redis.get(cache_key)
    if cached_review:
        logger.info(f"Return cached result")
        return {"review": cached_review}

    files = github_client.get_repo_files(str(review_request.github_repo_url))

    file_summaries = "\n\n".join(
        f"### {file['name']}:\n{file['content']}" for file in files
    )

    prompt = f"""
    Review the code for the following assignment:
    Assignment: {review_request.assignment_description}
    Candidate Level: {review_request.candidate_level}
    Files and content: 
    {file_summaries}.
    Return the review result in the following format:
    Found Files, Downsides/Comments, Rating, Conclusion
    """

    review = await openai_client.analyze_code(prompt)
    await redis.setex(cache_key, 3600, review)
    return {"review": review}


@review_router.get("/candidate-level-types")
async def candidate_level_types():
    return [lvl.value for lvl in CandidateLevel]
