from src.main.code_changes import collect_changes
from src.main.config import settings
from src.main.doc_map import build_doc_map
from src.main.inference import infer
from src.main.publish import gh, publish

if __name__ == "__main__":
    pr = gh.get_repo(settings.codebase_repo_path).get_pull(settings.pr_number)

    changes = collect_changes(pr, build_doc_map())
    updates = infer(changes)

    print(publish(updates, pr) or "no documentation updates")
