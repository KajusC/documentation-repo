import github
from github import Auth, Github, InputGitTreeElement

from src.main.config import settings

MARKER = "<!-- docs-bot -->"
CODE_PR = f"{settings.codebase_repo_path}#{settings.pr_number}"

gh = Github(auth=Auth.Token(settings.github_token))


def comment_on_pr(code_pr, text):
    body = f"{MARKER}\n{text}"
    me = gh.get_user().login
    for comment in code_pr.get_issue_comments():
        if comment.user.login == me and MARKER in comment.body:
            comment.edit(body)
            return
    code_pr.create_issue_comment(body)


def publish(updates, code_pr):
    if not updates:
        return None

    docs_repo = gh.get_repo(settings.documentation_repo_path)
    branch = f"docs/pr-{settings.pr_number}"

    try:
        head = docs_repo.get_branch(branch).commit.sha
    except github.GithubException:
        head = docs_repo.get_branch("main").commit.sha
        docs_repo.create_git_ref(f"refs/heads/{branch}", head)

    parent = docs_repo.get_git_commit(head)
    tree = docs_repo.create_git_tree(
        [
            InputGitTreeElement(
                u["path"], "100644", "blob", u["text"].rstrip("\n") + "\n"
            )
            for u in updates
        ],
        base_tree=parent.tree,
    )
    commit = docs_repo.create_git_commit(
        f"docs: updates from {CODE_PR}", tree, [parent]
    )
    docs_repo.get_git_ref(f"heads/{branch}").edit(commit.sha)

    pr = next(
        (p for p in docs_repo.get_pulls(state="open") if p.head.ref == branch), None
    )
    if pr is None:
        pr = docs_repo.create_pull(
            title=f"docs: updates from {CODE_PR}",
            body=f"Documentation updates for {CODE_PR}",
            head=branch,
            base="main",
        )

    files = "\n".join(f"- `{f.filename}`" for f in pr.get_files())
    comment_on_pr(code_pr, f"## Documentation updates\n\n{pr.html_url}\n\n{files}\n")
    return pr.html_url
