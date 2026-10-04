import re

import tree_sitter_c_sharp as tscs
from tree_sitter import Language, Parser, Query, QueryCursor

LANG = Language(tscs.language())
parser = Parser(LANG)
MEMBERS = Query(
    LANG,
    """
(method_declaration) @node
(constructor_declaration) @node
""",
)
HUNK = re.compile(r"^@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@")


def changed_new_lines(patch):
    lines = set()
    new = None
    for line in (patch or "").splitlines():
        match = HUNK.match(line)
        if match:
            new = int(match.group(2))
            continue
        if new is None:
            continue
        if line.startswith("+"):
            lines.add(new)
            new += 1
        elif not line.startswith("-"):
            new += 1
    return lines


def methods_from_patch(source, patch):
    changed = changed_new_lines(patch)
    found = []
    root = parser.parse(source).root_node
    for node in QueryCursor(MEMBERS).captures(root).get("node", []):
        start = node.start_point[0] + 1
        end = node.end_point[0] + 1
        if any(start <= line <= end for line in changed):
            found.append(
                {
                    "name": node.child_by_field_name("name").text.decode(),
                    "source": node.text.decode(),
                }
            )
    return found
