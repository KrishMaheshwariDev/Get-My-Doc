from pathlib import Path

# ==========================================
# Configuration
# ==========================================

OUTPUT_FILE = "structure.txt"

EXCLUDED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".idea",
    ".vscode",
    "dist",
    "build",
    "coverage",
    "logs",
    ".next",
    ".cache",
}

EXCLUDED_EXTENSIONS = {
    ".pyc",
    ".pyo",
    ".log",
    ".tmp",
    ".cache",
}

# ==========================================
# Tree Generator
# ==========================================

def generate_tree(path: Path, prefix: str = ""):
    items = sorted(
        path.iterdir(),
        key=lambda p: (not p.is_dir(), p.name.lower())
    )

    for index, item in enumerate(items):
        if item.is_dir() and item.name in EXCLUDED_DIRS:
            continue

        if item.is_file() and item.suffix in EXCLUDED_EXTENSIONS:
            continue

        connector = "└── " if index == len(items) - 1 else "├── "

        print(prefix + connector + item.name, file=output)

        if item.is_dir():
            extension = "    " if index == len(items) - 1 else "│   "
            generate_tree(item, prefix + extension)


# ==========================================
# Main
# ==========================================

root = Path.cwd()

with open(OUTPUT_FILE, "w", encoding="utf-8") as output:
    print(root.name, file=output)
    generate_tree(root)

print(f"Project structure written to '{OUTPUT_FILE}'")