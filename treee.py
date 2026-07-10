from pathlib import Path

# Folders/files to ignore
IGNORE_DIRS = {
    "venv",
    ".git",
    "__pycache__",
    "node_modules",
    ".idea",
    ".vscode",
    ".pytest_cache",
    "models",      # remove this line if you want models shown
}

IGNORE_FILES = {
    ".DS_Store",
}


def print_tree(path: Path, prefix=""):
    items = sorted(
        [p for p in path.iterdir()
         if p.name not in IGNORE_DIRS
         and p.name not in IGNORE_FILES],
        key=lambda x: (x.is_file(), x.name.lower())
    )

    for i, item in enumerate(items):
        connector = "└── " if i == len(items) - 1 else "├── "
        print(prefix + connector + item.name)

        if item.is_dir():
            extension = "    " if i == len(items) - 1 else "│   "
            print_tree(item, prefix + extension)


if __name__ == "__main__":
    root = Path(".")
    print(root.name)
    print_tree(root)