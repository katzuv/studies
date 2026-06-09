import subprocess
from pathlib import Path
from typing import Annotated

import typer

app = typer.Typer(add_completion=False)


@app.command()
def main(
    file_path: Annotated[
        Path,
        typer.Argument(
            help="Path to the Typst file to compile.",
            show_default=True,
        ),
    ] = Path("main.typ"),
    output: Annotated[
        str | None,
        typer.Option(
            "--output",
            "-o",
            help="Explicit PDF file name or path.",
        ),
    ] = None,
):
    """Compile Typst files to PDF with smart naming based on directory structure."""
    file_path = file_path.resolve()
    if not file_path.exists():
        if file_path == Path.cwd() / "main.typ":
            typer.echo("Usage: uv run tc.py <file.typ>")
        else:
            typer.echo(f"Error: File {file_path} not found.")
        raise typer.Exit(code=1)

    parent = file_path.parent
    if output:
        output_path = Path(output)
        if output_path.suffix.lower() != ".pdf":
            output_path = output_path.with_suffix(".pdf")
        if output_path.parent == Path("") or output_path.parent == Path("."):
            output_path = parent / output_path
        else:
            output_path = output_path.resolve()
    else:
        # Determine HW Number and Subject from directory structure
        # Path format example: 2026S/Quantum1/HW/HW02/main.typ
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

    try:
        relative_file = file_path.relative_to(Path.cwd())
    except ValueError:
        relative_file = file_path

    try:
        relative_output = output_path.relative_to(Path.cwd())
    except ValueError:
        relative_output = output_path

    typer.echo(f"Compiling {relative_file} -> {relative_output}...")

    try:
        subprocess.run(
            ["typst", "compile", "--root", ".", str(file_path), str(output_path)],
            check=True,
        )
        typer.echo("Success!")
    except subprocess.CalledProcessError:
        typer.echo("Compilation failed.")
        raise typer.Exit(code=1) from None


if __name__ == "__main__":
    app()
