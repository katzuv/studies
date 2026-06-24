import subprocess
import sys
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

app = typer.Typer(
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
)


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
    force: Annotated[
        bool,
        typer.Option(
            "--force",
            "-f",
            help="Force compilation of non-Typst files.",
        ),
    ] = False,
):
    """Compile Typst files to PDF with smart naming based on directory structure."""
    console = Console(highlight=False)

    try:
        sys.stdout.reconfigure(errors="replace")
        sys.stderr.reconfigure(errors="replace")
    except AttributeError:
        pass

    file_path = file_path.resolve()
    if not file_path.exists():
        if file_path == Path.cwd() / "main.typ":
            console.print(
                "[bold red]Error:[/bold red] No [cyan]main.typ[/cyan] found in the current directory."
            )
            console.print("[yellow]Usage:[/yellow] uv run tc <file.typ>")
        else:
            console.print(
                f"[bold red]Error:[/bold red] File [cyan]{file_path}[/cyan] not found."
            )
        raise typer.Exit(code=1)

    if file_path.suffix.lower() != ".typ" and not force:
        console.print(
            f"[bold yellow]Warning:[/bold yellow] The file [cyan]{file_path.name}[/cyan] does not have a [cyan].typ[/cyan] extension."
        )
        console.print(
            "Use [bold]--force[/bold] or [bold]-f[/bold] to compile it anyway."
        )
        raise typer.Exit(code=1)

    parent = file_path.parent

    # Locate project root dynamically
    project_root = None
    for p in [file_path] + list(file_path.parents):
        if (p / "pyproject.toml").exists() or (p / ".git").exists():
            project_root = p
            break

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

        # Subject is exactly two directories down from the project root
        subject = None
        if project_root:
            try:
                rel_parts = file_path.relative_to(project_root).parts
                if len(rel_parts) >= 3:
                    subject = rel_parts[1]
            except ValueError:
                pass

        filename = f"{subject} – {hw_number}.pdf" if subject else f"{hw_number}.pdf"

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

    console.print(
        f"[bold blue]Compiling:[/bold blue] [cyan]{relative_file}[/cyan] [dim]→[/dim] [green]{relative_output}[/green]"
    )

    try:
        subprocess.run(
            [
                "typst",
                "--color",
                "always",
                "compile",
                "--root",
                str(project_root) if project_root else ".",
                str(file_path),
                str(output_path),
            ],
            capture_output=True,
            check=True,
        )
        console.print("[bold green]✓ Success![/bold green]")
    except subprocess.CalledProcessError as e:
        stderr_str = e.stderr.decode("utf-8", errors="replace")
        error_text = Text.from_ansi(stderr_str.strip())
        console.print(
            Panel(
                error_text,
                title="[bold red]Typst Compilation Error[/bold red]",
                border_style="red",
                expand=False,
            )
        )
        raise typer.Exit(code=1) from None


if __name__ == "__main__":
    app()
