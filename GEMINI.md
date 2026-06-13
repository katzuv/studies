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
    - **No Graph Titles:** Experimental graphs must **never** include a title within the image itself. Captions must be used in the report instead.
- **Typst Standards:**
    - **Native Syntax:** Never use backslashes (`\`) before functions or symbols in Typst (this is not LaTeX). 
    - **Math Mode:** Use native function calls (e.g., `ket(psi)`, `braket(a, b)`, `prop`, `quad`) instead of LaTeX-style commands.
    - **Labels:** To use labels in math as function arguments (like `ket(theta, d)`), escape the comma with a backslash if it causes ambiguity: `ket(theta\, d)`.
- **Linting & Style:**
    - Use **Ruff** for formatting and linting.
    - Exclude legacy semester directories from linting: `2025S`, `2025W`, `2026W`.

## Typst Templates
- **Lab Template:** Located at `typst/templates/lab.typ`.
- **Requirements:** Uses three **positional required parameters**: `experiment_name`, `instructor`, and `course_name`.

## Homework Workflow
- When copying questions and clauses from course materials into Typst files:
    - **Always** use the `מזהה` (identifier) parameter for all `שאלה` and `סעיף` function calls.
    - The value should be a label (e.g., `<4.3>`) corresponding to the question/clause number.
    - **Nested Labels:** Use dots for nested references (e.g., `<2.2.ב>`). The template is configured to parse these and display them as "שאלה 2 סעיף 2.ב".
    - **No Manual Pagebreaks:** Do not add manual `#pagebreak()` calls after `#תשובה`. The `#שאלה` function automatically handles pagination for each new question.
    - Example: `#סעיף(מזהה: <4.3>, [טקסט])` (Reference: `2026S/Quantum1/HW/HW03/main.typ`)
    - **Typst Compilation Rule:** If the USER makes edits to Typst files, do NOT compile the files (the user will compile them). However, if the AGENT makes the edits to Typst files, the agent MUST run the compiler to check for syntax and layout errors.

