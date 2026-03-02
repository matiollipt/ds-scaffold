#!/usr/bin/env python3
"""
ds-scaffold.py
==============

ds-scaffold a new data science / ML project with a standard folder structure,
AI context files (AGENTS.md, CONTEXT.md, dev-notes.md), and Python module
stubs following PEP 8 / PEP 257 conventions.

Usage
-----
    python ds-scaffold.py <project-name> [OPTIONS]

Examples
--------
    python ds-scaffold.py my-analysis
    python ds-scaffold.py rna-seq-pipeline --author "Jane Doe" --desc "RNA-Seq differential expression pipeline"

Author
------
    <your name>

License
-------
    MIT
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
)
from rich.table import Table
from rich.theme import Theme

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

custom_theme = Theme(
    {
        "info": "bold cyan",
        "success": "bold green",
        "warning": "bold yellow",
        "error": "bold red",
        "muted": "dim white",
        "header": "bold white on dark_blue",
    }
)

console = Console(theme=custom_theme)
app = typer.Typer(
    name="ds-scaffold",
    help="ds-scaffold a new DS/ML project with AI context files and Python stubs.",
    add_completion=False,
)

TODAY = date.today().isoformat()


# ---------------------------------------------------------------------------
# File content generators
# ---------------------------------------------------------------------------


def _agents_md(project: str, description: str, author: str) -> str:
    return f"""\
# AGENTS.md
> AI briefing document — paste this at the start of every AI session.

## Project
{description if description else f"[One sentence: what {project} does and why]"}

## Author
{author if author else "[Your name]"}

## Stack
- Python 3.11+
- Data: pandas / polars, numpy
- ML: scikit-learn
- CLI: Typer + Rich
- Visualization: matplotlib / plotly
- Testing: pytest
- Linting: ruff

## Conventions
- Functions: `snake_case`, typed signatures, Google-style docstrings
- Files stay under 300 lines; split if longer
- CLI via Typer; use `logging` module, never bare `print()`
- All plots saved to `reports/figures/` as PNG + interactive Plotly HTML
- Raw data is **never** modified in-place

## Never Do
- Don't use global state
- Don't hardcode paths — use `pathlib` and config objects
- Don't write to `data/raw/`
- Don't add dependencies without flagging it first
- Don't use `df.apply()` when a vectorised alternative exists

## Current Task
[Update this each session: describe what you are working on right now]
"""


def _context_md(project: str, description: str) -> str:
    return f"""\
# CONTEXT.md
> Living project state — update at the end of every AI session.

## Project
**{project}** — {description if description else "[short description]"}

## Last Updated
{TODAY}

## What's Done
- [ ] Data ingestion pipeline (`src/ingest.py`)
- [ ] Processing / feature engineering (`src/process.py`)
- [ ] Analysis / modelling (`src/analyze.py`)
- [ ] Visualizations (`src/visualize.py`)
- [ ] CLI entry point (`cli.py`)
- [ ] Tests (`tests/`)
- [ ] README

## Current Blockers
_None yet — add blockers here as they arise._

## Key Files
| File | Purpose |
|---|---|
| `src/ingest.py` | Raw data loading and schema validation |
| `src/process.py` | Cleaning, normalisation, feature engineering |
| `src/analyze.py` | EDA, statistics, model training |
| `src/visualize.py` | All plot generation |
| `cli.py` | Typer CLI entry point |
| `data/raw/` | Source data — never modify |
| `data/processed/` | Final clean datasets |
| `reports/figures/` | All saved plots |

## Key Decisions
| Date | Decision | Reason |
|---|---|---|
| {TODAY} | Project ds-scaffolded | Initial setup |

## Next Session: Start Here
Review `AGENTS.md` and this file, then begin with data ingestion in `src/ingest.py`.
Test with: `python cli.py ingest --input data/raw/<your-file> --dry-run`
"""


def _dev_notes_md(project: str) -> str:
    return f"""\
# dev-notes.md
> Personal scratch pad — prompt log, architectural notes, AI failure patterns.

## Project
{project}

## Working Prompts

### New function / module
```
Write a Python function for [task].
Input: [type and description].
Output: [type and description].
Edge cases: [list].
Use typed signatures, Google docstrings, raise ValueError for bad input.
Stack: [polars | pandas], pathlib, Python 3.11.
```

### Pipeline debugging
```
I have a Python pipeline: [paste code].
Input: [describe]. Expected output: [describe].
Actual output / error: [paste traceback].
Constraints: [e.g. can't change the schema].
What is wrong and how do I fix it?
```

### EDA / visualisation
```
I have a dataset with these columns: [schema].
I want to understand: [specific question].
Write a function that computes [stats / plot].
Save figure to reports/figures/eda_[name].png at 300 DPI.
Use matplotlib, minimal style, Arial font.
```

### Multi-file refactor (Aider)
```
/add src/ingest.py src/process.py cli.py
Refactor so all functions accept a Config dataclass instead of
individual keyword arguments. Create src/config.py.
```

## Architectural Decisions
| Date | Decision | Reason |
|---|---|---|
| {TODAY} | Initial ds-scaffolding | Project created |

## AI Gotchas in This Project
- [ ] Add entries here when an AI tool produces wrong API calls or bad patterns

## Useful Commands
```bash
# Lint
ruff check src/ && ruff format --check src/

# Run tests
pytest tests/ -v

# Aider with free Gemini API
aider --model gemini/gemini-2.0-flash --no-auto-commits

# Local model via Ollama
aider --model ollama/qwen2.5-coder:7b --no-auto-commits
```
"""


def _python_stub(module: str, description: str, project: str, author: str) -> str:
    """Return a PEP 8 / PEP 257 compliant Python module stub."""
    return f"""\
#!/usr/bin/env python3
\"\"\"
{module}.py
{'=' * (len(module) + 3)}

{description}

Typical usage
-------------
    from src.{module} import ...

Notes
-----
- Follow AGENTS.md conventions: typed signatures, Google docstrings,
  no global state, no hardcoded paths.
- Do not modify data/raw/ — always write to data/interim/ or data/processed/.

Author
------
    {author if author else "[Your name]"}

Created
-------
    {TODAY}
\"\"\"

from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def main() -> None:
    \"\"\"Entry point for ad-hoc module execution.\"\"\"
    logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
    logger.info("Running {module} module directly — replace with real logic.")


if __name__ == "__main__":
    main()
"""


def _cli_stub(project: str, author: str) -> str:
    return f"""\
#!/usr/bin/env python3
\"\"\"
cli.py
======

Command-line interface for **{project}**.

Provides sub-commands for each pipeline stage: ingest, process,
analyze, and visualize.  Uses Typer for argument parsing and Rich
for formatted output.

Usage
-----
    python cli.py --help
    python cli.py ingest --input data/raw/sample.csv --dry-run
    python cli.py process --input data/interim/clean.parquet
    python cli.py analyze --input data/processed/features.parquet
    python cli.py visualize --input data/processed/features.parquet

Author
------
    {author if author else "[Your name]"}

Created
-------
    {TODAY}
\"\"\"

from __future__ import annotations

import logging
from pathlib import Path

import typer
from rich.console import Console
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
logger = logging.getLogger(__name__)
console = Console()
app = typer.Typer(
    name="{project}",
    help="Pipeline CLI for {project}.",
    add_completion=False,
)


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


@app.command()
def ingest(
    input: Path = typer.Option(..., "--input", "-i", help="Path to raw input file."),
    dry_run: bool = typer.Option(False, "--dry-run", help="Validate only, do not write."),
) -> None:
    \"\"\"Load raw data, validate schema, and save to data/interim/.\"\"\"
    console.print(f"[bold cyan]Ingest[/] {{input}}" + (" [dim](dry run)[/]" if dry_run else ""))
    # TODO: implement — import from src/ingest.py
    raise NotImplementedError("Implement src/ingest.py first.")


@app.command()
def process(
    input: Path = typer.Option(..., "--input", "-i", help="Path to interim data file."),
) -> None:
    \"\"\"Clean, normalise, and engineer features.  Writes to data/processed/.\"\"\"
    console.print(f"[bold cyan]Process[/] {{input}}")
    # TODO: implement — import from src/process.py
    raise NotImplementedError("Implement src/process.py first.")


@app.command()
def analyze(
    input: Path = typer.Option(..., "--input", "-i", help="Path to processed data file."),
) -> None:
    \"\"\"Run EDA, statistics, or model training.\"\"\"
    console.print(f"[bold cyan]Analyze[/] {{input}}")
    # TODO: implement — import from src/analyze.py
    raise NotImplementedError("Implement src/analyze.py first.")


@app.command()
def visualize(
    input: Path = typer.Option(..., "--input", "-i", help="Path to processed data file."),
    output_dir: Path = typer.Option(Path("reports/figures"), "--output-dir", "-o"),
) -> None:
    \"\"\"Generate and save all project figures.\"\"\"
    console.print(f"[bold cyan]Visualize[/] {{input}} → {{output_dir}}")
    # TODO: implement — import from src/visualize.py
    raise NotImplementedError("Implement src/visualize.py first.")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app()
"""


def _pyproject_toml(project: str, author: str) -> str:
    safe = project.lower().replace(" ", "-").replace("_", "-")
    return f"""\
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.backends.legacy:build"

[project]
name = "{safe}"
version = "0.1.0"
description = "Data science project: {project}"
authors = [{{name = "{author if author else 'Author'}"}}]
requires-python = ">=3.11"
dependencies = [
    "typer[all]",
    "rich",
    "pandas",
    "polars",
    "numpy",
    "matplotlib",
    "plotly",
    "scikit-learn",
]

[project.optional-dependencies]
dev = ["pytest", "ruff", "ipykernel"]

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "D"]
ignore = ["D203", "D213"]

[tool.pytest.ini_options]
testpaths = ["tests"]
"""


def _gitignore() -> str:
    return """\
# Python
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.venv/
venv/
.env

# Data (raw data should not be committed unless small)
data/raw/
data/interim/
data/processed/

# Reports / outputs
reports/figures/
*.png
*.html

# Jupyter
.ipynb_checkpoints/
*.ipynb

# IDE
.vscode/
.idea/
*.code-workspace

# OS
.DS_Store
Thumbs.db
"""


def _readme(project: str, description: str, author: str) -> str:
    return f"""\
# {project}

{description if description else "> [Add a one-paragraph project description here]"}

## Setup

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\\Scripts\\activate
pip install -e ".[dev]"
```

## Usage

```bash
python cli.py --help
python cli.py ingest  --input data/raw/<file>
python cli.py process --input data/interim/<file>
python cli.py analyze --input data/processed/<file>
python cli.py visualize --input data/processed/<file>
```

## Project Structure

```
{project}/
├── AGENTS.md          # AI briefing document
├── CONTEXT.md         # Living project state
├── dev-notes.md       # Prompt log and decisions
├── cli.py             # CLI entry point
├── data/
│   ├── raw/           # Source data — never modified
│   ├── interim/       # Mid-processing
│   └── processed/     # Final clean data
├── src/
│   ├── ingest.py
│   ├── process.py
│   ├── analyze.py
│   └── visualize.py
├── notebooks/         # Exploration only
├── reports/figures/   # Saved plots
├── tests/
├── pyproject.toml
└── .gitignore
```

## Author
{author if author else "[Your name]"}

## License
MIT
"""


def _test_stub(module: str) -> str:
    return f"""\
\"\"\"Tests for src/{module}.py.\"\"\"

from __future__ import annotations

import pytest


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


# @pytest.fixture
# def sample_df():
#     import polars as pl
#     return pl.DataFrame({{"col_a": [1, 2, 3]}})


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_placeholder() -> None:
    \"\"\"Placeholder — replace with real tests for src/{module}.py.\"\"\"
    assert True
"""


# ---------------------------------------------------------------------------
# ds-scaffold logic
# ---------------------------------------------------------------------------


def build_manifest(
    root: Path, project: str, description: str, author: str
) -> list[tuple[Path, str]]:
    """Return a list of (path, content) pairs for all files to create."""
    src = root / "src"
    tests = root / "tests"

    modules = ["ingest", "process", "analyze", "visualize"]
    module_descriptions = {
        "ingest": "Raw data loading, schema validation, and persistence to data/interim/.",
        "process": "Data cleaning, normalisation, and feature engineering.",
        "analyze": "Exploratory data analysis, statistical tests, and model training.",
        "visualize": "Figure generation and saving for reports and presentations.",
    }

    manifest: list[tuple[Path, str]] = [
        # AI context files
        (root / "AGENTS.md", _agents_md(project, description, author)),
        (root / "CONTEXT.md", _context_md(project, description)),
        (root / "dev-notes.md", _dev_notes_md(project)),
        # Project files
        (root / "README.md", _readme(project, description, author)),
        (root / "pyproject.toml", _pyproject_toml(project, author)),
        (root / ".gitignore", _gitignore()),
        (root / "cli.py", _cli_stub(project, author)),
        # src modules
        (
            src / "__init__.py",
            '"""Source package for {project}."""\n'.replace("{project}", project),
        ),
        *[
            (src / f"{m}.py", _python_stub(m, module_descriptions[m], project, author))
            for m in modules
        ],
        # tests
        (tests / "__init__.py", ""),
        *[(tests / f"test_{m}.py", _test_stub(m)) for m in modules],
    ]
    return manifest


DIRS = [
    "data/raw",
    "data/interim",
    "data/processed",
    "src",
    "notebooks",
    "reports/figures",
    "tests",
]


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


@app.command()
def ds_scaffold(
    project_name: str = typer.Argument(
        ..., help="Name of the new project (used as folder name)."
    ),
    author: str = typer.Option(
        "", "--author", "-a", help="Author name for file headers."
    ),
    description: str = typer.Option(
        "", "--desc", "-d", help="One-line project description."
    ),
    output_dir: Path = typer.Option(
        Path("."), "--output", "-o", help="Parent directory for the project."
    ),
    force: bool = typer.Option(
        False, "--force", "-f", help="Overwrite existing files without prompting."
    ),
) -> None:
    """
    ds-scaffold a new DS/ML project folder with AI context files and Python stubs.
    """
    root = output_dir / project_name

    # --- Header banner ---
    console.print()
    console.print(
        Panel.fit(
            f"[bold white]ds-scaffold[/]  ·  DS/ML Project ds-scaffolder\n"
            f"[muted]Creating:[/] [bold cyan]{root}[/]",
            border_style="dark_blue",
            padding=(0, 2),
        )
    )
    console.print()

    # --- Guard: existing directory ---
    if root.exists() and not force:
        console.print(f"[warning]⚠  Directory already exists:[/] {root}")
        overwrite = typer.confirm("Overwrite existing files?", default=False)
        if not overwrite:
            console.print("[muted]Aborted.[/]")
            raise typer.Exit(0)

    # --- Step 1: Create directories ---
    console.print("[info]❶  Creating directory structure…[/]")
    dirs_to_create = [root / d for d in DIRS]

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=30),
        TaskProgressColumn(),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task("Directories", total=len(dirs_to_create))
        for d in dirs_to_create:
            d.mkdir(parents=True, exist_ok=True)
            (d / ".gitkeep").touch()
            progress.advance(task)

    console.print(f"   [success]✔[/]  {len(dirs_to_create)} directories ready\n")

    # --- Step 2: Write files ---
    console.print("[info]❷  Writing files…[/]")
    manifest = build_manifest(root, project_name, description, author)

    created, skipped = 0, 0

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description:<40}"),
        BarColumn(bar_width=30),
        TaskProgressColumn(),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task("Files", total=len(manifest))
        for path, content in manifest:
            progress.update(task, description=f"[muted]{path.relative_to(root)}[/]")
            if path.exists() and not force:
                skipped += 1
            else:
                path.write_text(content, encoding="utf-8")
                created += 1
            progress.advance(task)

    console.print(
        f"   [success]✔[/]  {created} files written"
        + (f", {skipped} skipped" if skipped else "")
        + "\n"
    )

    # --- Step 3: Summary table ---
    console.print("[info]❸  Project summary[/]\n")

    table = Table(
        show_header=True,
        header_style="header",
        border_style="bright_black",
        expand=False,
    )
    table.add_column("Category", style="bold cyan", min_width=18)
    table.add_column("Path", style="white")
    table.add_column("Purpose", style="dim white")

    table.add_row("AI Briefing", "AGENTS.md", "Paste at start of every AI session")
    table.add_row("AI State", "CONTEXT.md", "Update after every session")
    table.add_row("Prompt Log", "dev-notes.md", "Prompts, decisions, AI gotchas")
    table.add_row("CLI", "cli.py", "Typer entry point")
    table.add_row("Ingest", "src/ingest.py", "Raw data loading & validation")
    table.add_row("Process", "src/process.py", "Cleaning & feature engineering")
    table.add_row("Analyze", "src/analyze.py", "EDA, stats, modelling")
    table.add_row("Visualize", "src/visualize.py", "Figure generation")
    table.add_row("Tests", "tests/", "pytest stubs for each module")

    console.print(table)
    console.print()

    # --- Next steps ---
    console.print(
        Panel(
            "[bold white]Next steps[/]\n\n"
            f"  [cyan]cd {root}[/]\n"
            "  [cyan]python -m venv .venv && source .venv/bin/activate[/]\n"
            "  [cyan]pip install -e '.[dev]'[/]\n\n"
            "  [dim]Then open AGENTS.md and fill in your project description.[/]\n"
            "  [dim]Git init:[/] [cyan]git init && git add . && git commit -m 'chore: initial ds-scaffold'[/]",
            border_style="green",
            padding=(0, 2),
        )
    )
    console.print()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """Entry point for the ds-scaffold CLI."""
    app()


if __name__ == "__main__":
    main()
