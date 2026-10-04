from pathlib import Path


def list_files(startpath):
    root = Path(startpath)
    lines = []
    for directory, dirnames, filenames in root.walk():
        dirnames.sort()
        filenames.sort()
        depth = len(directory.relative_to(root).parts)
        lines.append(f"{'    ' * depth}{directory.name}/")
        lines.extend(f"{'    ' * (depth + 1)}{name}" for name in filenames)
    return "\n".join(lines)
