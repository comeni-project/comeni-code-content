# /// script
# requires-python = ">=3.12"
# ///
"""The `review` check for comeni-code-content (Comeni Code's M4.6 spec, M4L.6).

A pull request opened by Comeni Code's Studio app, or by a maintainer, passes: Studio reviewed it,
and a maintainer is trusted. Anyone else's passes only once a maintainer has approved it. The
lists are read from main through the API, never from the pull request, which could edit them. The
result is posted as the commit status `review` on the pull request's head.
Run by .github/workflows/review.yml, with GITHUB_TOKEN, GITHUB_API_URL, GITHUB_REPOSITORY and
PR_NUMBER set.
"""

import base64
import json
import os
import sys
import urllib.error
import urllib.request

API = os.environ["GITHUB_API_URL"]
REPO = os.environ["GITHUB_REPOSITORY"]
TOKEN = os.environ["GITHUB_TOKEN"]
NUMBER = os.environ["PR_NUMBER"]


def call(method: str, path: str, body: object = None) -> object:
    request = urllib.request.Request(
        f"{API}/repos/{REPO}{path}",
        method=method,
        data=None if body is None else json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github+json"},
    )
    with urllib.request.urlopen(request, timeout=30) as answer:
        text = answer.read()
    return json.loads(text) if text else None


def listed(path: str) -> set[str]:
    """The logins in a file on main: one per line, `#` for comments; empty if it is missing."""
    try:
        found = call("GET", f"/contents/{path}?ref=main")
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return set()
        raise
    assert isinstance(found, dict)
    text = base64.b64decode(found["content"]).decode()
    return {
        line.strip().lower()
        for line in text.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }


def main() -> int:
    pull = call("GET", f"/pulls/{NUMBER}")
    assert isinstance(pull, dict)
    author = pull["user"]["login"].lower()
    maintainers = listed("MAINTAINERS")
    if author in listed(".github/studio-app"):
        state, words = "success", "Opened by Studio, which reviewed it."
    elif author in maintainers:
        state, words = "success", "Opened by a maintainer."
    else:
        reviews = call("GET", f"/pulls/{NUMBER}/reviews?per_page=100")
        assert isinstance(reviews, list)
        latest = {
            review["user"]["login"].lower(): review["state"]
            for review in reviews
            if review["state"] != "COMMENTED"
        }
        if any(latest.get(login) == "APPROVED" for login in maintainers):
            state, words = "success", "A maintainer approved it."
        else:
            state, words = "failure", "Needs a maintainer's approval."
    call(
        "POST",
        f"/statuses/{pull['head']['sha']}",
        {"state": state, "context": "review", "description": words},
    )
    print(words)
    return 0


if __name__ == "__main__":
    sys.exit(main())
