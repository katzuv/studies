# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///

import subprocess
import sys
from pathlib import Path


def compile_typst(file_path_str: str):
    file_path = Path(file_path_str).resolve()
    if not file_path.exists():
        print(f"Error: File {file_path} not found.")
        return

    # Determine HW Number and Subject from directory structure
    # Path format example: 2026S/Quantum1/HW/HW02/main.typ
    parent = file_path.parent
    hw_number = parent.name

    # Subject is the first ancestor that isn't 'HW', 'HWs', or 'Numeric'
    subject = "document"
    for ancestor in parent.parents:
        # Stop at project root (assuming tc.py is at root)
        if ancestor == Path.cwd():
            break
        name_lower = ancestor.name.lower()
        if name_lower not in ("hw", "hws", "numeric"):
            subject = ancestor.name
            break

    filename = f"{subject} {hw_number}.pdf"

    # Clean filename for OS compatibility
    for char in '<>:"/\\|?*':
        filename = filename.replace(char, "-")

    output_path = parent / filename

    print(
        f"Compiling {file_path.relative_to(Path.cwd())} -> {output_path.relative_to(Path.cwd())}..."
    )

    try:
        subprocess.run(
            ["typst", "compile", "--root", ".", str(file_path), str(output_path)],
            check=True,
        )
        print("Success!")
    except subprocess.CalledProcessError:
        print(f"Compilation failed.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Default to main.typ in current dir if no arg provided
        target = Path("main.typ")
        if target.exists():
            compile_typst(str(target))
        else:
            print("Usage: uv run tc.py <file.typ>")
    else:
        compile_typst(sys.argv[1])
