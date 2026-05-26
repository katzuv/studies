# Project Mandates

## Python Environment
- **Project Name:** `studies`
- **Minimum Python Version:** `3.14`
- **Package Management:** Use **uv** and **hatch**.

## Engineering Standards
- **Physics Library (`physlab`):**
    - Generic physics tools (fitting, styling, error propagation) must reside in the root `physlab` package.
    - Experiment-specific logic must be kept in the local experiment directory (e.g., `analysis_tools.py`).
- **Graphics Standard:**
    - All experimental graphs **must always** be saved in **SVG** format. No exceptions.
- **Linting & Style:**
    - Use **Ruff** for formatting and linting.
    - Exclude legacy semester directories from linting: `2025S`, `2025W`, `2026W`.

## Typst Templates
- **Lab Template:** Located at `typst/templates/lab.typ`.
- **Requirements:** Uses three **positional required parameters**: `experiment_name`, `instructor`, and `course_name`.
