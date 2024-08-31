# https://python-gitlab.readthedocs.io/en/stable/api-usage.html
import logging
import os
from typing import Optional

import git
import gitlab
import gitlab.client
import gitlab.types
from gitlab.exceptions import GitlabGetError
from gitlab.v4.objects.merge_requests import ProjectMergeRequest
from gitlab.v4.objects.projects import Project


def getenv(name) -> Optional[str]:
    return os.environ.get(name)


DEFAULT_SERVER = "https://gitlab.kudelski.com"

# https://docs.gitlab.com/ee/ci/variables/predefined_variables.html
CI_API_URL = getenv("CI_API_V4_URL") or DEFAULT_SERVER
CI_PROJECT_ID = getenv("CI_PROJECT_ID")  # CI_MERGE_REQUEST_PROJECT_ID
CI_MERGE_REQUEST_ID = getenv("CI_MERGE_REQUEST_ID")
CI_MERGE_REQUEST_IID = getenv("CI_MERGE_REQUEST_IID")


def get_api_token():
    getenv("CI_JOB_TOKEN")
    getenv("GITLAB_TOKEN")


def gitlab_client(
    server: Optional[str] = None,
    api_key: Optional[str] = None,
    raise_exception=False,
) -> Optional[gitlab.Gitlab]:
    if not server:
        server = CI_API_URL
    if not server:
        logging.debug("Missing server")
        return None
    if not api_key:
        api_key = getenv("GITLAB_TOKEN")
    if not api_key:
        logging.debug("Missing api key")
        return None
    try:
        gl = gitlab.Gitlab(url=server, private_token=api_key)
        gl.auth()
    except Exception as e:
        if not raise_exception:
            logging.debug(f"Failed authentication: {e}")
            return None
        logging.error(
            "Authentication Failed. "
            "Check the server and access token passed to the script",
        )
        raise
    return gl


def gitlab_project(
    repo: Optional[str] = None,
    server: Optional[str] = None,
    api_key: Optional[str] = None,
    raise_exception=False,
) -> Optional[Project]:
    if not repo:
        repo = CI_PROJECT_ID
    if not repo:
        return None
    repo = repo.strip("/")
    if not repo:
        logging.debug("Missing repo")
        return None
    gl = gitlab_client(server, api_key, raise_exception=raise_exception)
    if not gl:
        return None
    try:
        return gl.projects.get(repo)
    except GitlabGetError:
        if not raise_exception:
            logging.debug("Repo does not exists")
            return None
        logging.error("Project does not exists")
        raise


def gitlab_mr(
    mr_id=None,
    repo: Optional[str] = None,
    server: Optional[str] = None,
    api_key: Optional[str] = None,
    raise_exception=False,
) -> Optional[ProjectMergeRequest]:
    if not mr_id:
        mr_id = CI_MERGE_REQUEST_IID
    if not mr_id:
        logging.debug("Missing merge request ID")
        return None
    project = gitlab_project(repo, server, api_key, raise_exception=raise_exception)
    if project is None:
        return None
    return project.mergerequests.get(mr_id)


def add_mr_comment(
    comment: str,
    mr_id=None,
    repo: Optional[str] = None,
    server: Optional[str] = None,
    api_key: Optional[str] = None,
    raise_exception=False,
) -> Optional[dict]:
    mr = gitlab_mr(mr_id, repo, server, api_key, raise_exception=raise_exception)
    if not mr:
        return None
    return mr.notes.create({"body": comment}).asdict()


def get_diff(repo=None) -> str:
    git_repo = git.Repo(repo)
    return git_repo.git.diff()


DEFAULT_DIFF_COMMENT = """\
Error while executing the pipeline. The following changes where found:
```diff
{diff}
```
"""


def post_git_diff(message: str = DEFAULT_DIFF_COMMENT, repo=None):
    diff = get_diff(repo)
    if diff:
        add_mr_comment(message.format(diff=diff))
