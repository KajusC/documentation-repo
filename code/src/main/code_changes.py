from src.main.config import REPO_ROOT
from src.main.csharp_methods import methods_from_patch


def collect_changes(pr, doc_map):
    changes = []
    for f in pr.get_files():
        pages = [
            {"path": path, "text": (REPO_ROOT / path).read_text(encoding="utf-8")}
            for path in doc_map.get(f.filename, [])
        ]
        change = {
            "path": f.filename,
            "status": f.status,
            "patch": f.patch or "",
            "pages": pages,
            "methods": [],
        }
        if f.filename.endswith(".cs") and f.status != "removed":
            source = pr.base.repo.get_contents(f.filename, ref=pr.head.sha)
            change["methods"] = methods_from_patch(
                source.decoded_content, change["patch"]
            )
        changes.append(change)
    return changes
