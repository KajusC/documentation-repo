import re

from src.main.config import DOCS_DIR, REPO_ROOT

CODE_PATH = re.compile(r"`([^`]+)`")
SKIP_PREFIXES = ("python_env/", "documents/")


def parse_sources(text):
    paths = []
    in_sources = False
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("## "):
            in_sources = line == "## Sources"
        elif in_sources:
            for raw in CODE_PATH.findall(line):
                path = raw.strip().replace("\\", "/")
                if path and not path.startswith(SKIP_PREFIXES):
                    paths.append(path)
    return list(dict.fromkeys(paths))


def build_doc_map():
    doc_map = {}
    for page in sorted(DOCS_DIR.glob("**/*.md")):
        doc_path = page.relative_to(REPO_ROOT).as_posix()
        for code_path in parse_sources(page.read_text(encoding="utf-8")):
            doc_map.setdefault(code_path, []).append(doc_path)
    return dict(sorted(doc_map.items()))
