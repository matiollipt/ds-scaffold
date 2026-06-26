#!/usr/bin/env python3
"""
ds_scaffold.main
================

CLI entry point for ds-scaffold.

Scaffolds a new Data Science / ML project with:
- Standard folder layout  (data/, src/, tests/, notebooks/, reports/)
- AI context files        (AGENTS.md, CONTEXT.md, dev-notes.md)
- PEP 8 / PEP 257 Python module stubs
- Typer CLI skeleton, pyproject.toml, .gitignore, README.md

Usage
-----
    # After `uv tool install ds-scaffold` or `pip install -e .`
    ds-scaffold my-project
    ds-scaffold rna-seq --author "Jane Doe" --desc "RNA-Seq DE pipeline"
    ds-scaffold my-project --output ~/projects --force

Author
------
    ds-scaffold contributors

License
-------
    MIT
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Optional

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

from ds_scaffold import __version__

# ---------------------------------------------------------------------------
# App & console setup
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
    help="Scaffold a new Data Science project with AI-ready context and best practices.",
    add_completion=False,
    no_args_is_help=True,
)

TODAY = date.today().isoformat()


# ---------------------------------------------------------------------------
# Version callback
# ---------------------------------------------------------------------------


def _version_callback(value: bool) -> None:
    if value:
        console.print(f"ds-scaffold [bold cyan]v{__version__}[/]")
        raise typer.Exit()


# ---------------------------------------------------------------------------
# File content generators
# ---------------------------------------------------------------------------


def _agents_md(project: str, description: str, author: str) -> str:
    desc = (
        description if description else f"[One sentence: what {project} does and why]"
    )
    auth = author if author else "[Your name]"
    return f"""\
# AGENTS.md
> AI briefing document — paste this at the start of every AI session.

## Project
{desc}

## Author
{auth}

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
    desc = description if description else "[short description]"
    return f"""\
# CONTEXT.md
> Living project state — update at the end of every AI session.

## Project
**{project}** — {desc}

## Last Updated
{TODAY}

## What's Done
- [ ] Data ingestion pipeline (`{project}/ingest.py`)
- [ ] Processing / feature engineering (`{project}/process.py`)
- [ ] Analysis / modelling (`{project}/analyze.py`)
- [ ] Visualizations (`{project}/visualize.py`)
- [ ] CLI entry point (`cli.py`)
- [ ] Tests (`tests/`)
- [ ] README

## Current Blockers
_None yet — add blockers here as they arise._

## Key Files
| File | Purpose |
|---|---|
| `{project}/ingest.py` | Raw data loading and schema validation |
| `{project}/process.py` | Cleaning, normalisation, feature engineering |
| `{project}/analyze.py` | EDA, statistics, model training |
| `{project}/visualize.py` | All plot generation |
| `cli.py` | Typer CLI entry point |
| `data/raw/` | Source data — never modify |
| `data/processed/` | Final clean datasets |
| `reports/figures/` | All saved plots |

## Key Decisions
| Date | Decision | Reason |
|---|---|---|
| {TODAY} | Project scaffolded | Initial setup |

## Next Session: Start Here
Review `AGENTS.md` and this file, then begin with data ingestion in `{project}/ingest.py`.
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
/add {project}/ingest.py {project}/process.py cli.py
Refactor so all functions accept a Config dataclass instead of
individual keyword arguments. Create {project}/config.py.
```

## Architectural Decisions
| Date | Decision | Reason |
|---|---|---|
| {TODAY} | Initial scaffolding | Project created |

## AI Gotchas in This Project
- [ ] Add entries here when an AI tool produces wrong API calls or bad patterns

## Useful Commands
```bash
# Lint
ruff check {project}/ && ruff format --check {project}/

# Run tests
pytest tests/ -v

# Aider with free Gemini API
aider --model gemini/gemini-2.0-flash --no-auto-commits

# Local model via Ollama
aider --model ollama/qwen2.5-coder:7b --no-auto-commits
```
"""


def _utils_py(project: str) -> str:
    return f"""\
\"\"\"
{project}/utils.py
==================

Shared utilities, types, and logging configuration.
\"\"\"
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd


@dataclass
class AnalysisResult:
    \"\"\"Container for analysis artifacts.\"\"\"
    pca_components: np.ndarray
    pca_loadings: pd.DataFrame
    cluster_labels: np.ndarray
    corr: pd.DataFrame
    artifacts: dict[str, Path] = field(default_factory=dict)


def get_logger(name: str) -> logging.Logger:
    \"\"\"Get a configured logger.\"\"\"
    logger = logging.getLogger(name)
    # Handlers are configured in cli.py via basicConfig
    return logger


def load_data(path: Path, **kwargs) -> pd.DataFrame:
    \"\"\"Load data from parquet, csv, or tsv based on extension.\"\"\"
    ext = path.suffix.lower()
    if ext == ".parquet":
        return pd.read_parquet(path, **kwargs)
    elif ext in [".csv", ".txt", ".tsv"]:
        sep = "\\t" if ext == ".tsv" else None
        df = pd.read_csv(
            path,
            sep=sep,
            engine="python",
            skipinitialspace=True,
            on_bad_lines="warn",
            **kwargs
        )
        return df.loc[:, ~df.columns.str.contains("^Unnamed")]
    else:
        raise ValueError(f"Unsupported file extension: {{ext}}")
"""


def _ingest_py(project: str) -> str:
    return f"""\
\"\"\"
{project}/ingest.py
===================

Raw data loading, schema validation, and persistence.
\"\"\"
from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

import pandas as pd

from {project}.utils import get_logger, load_data

logger = get_logger(__name__)


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    \"\"\"Convert columns to snake_case and deduplicate.\"\"\"
    new_cols = []
    seen: dict[str, int] = {{}}

    for col in df.columns:
        # Lowercase and replace non-alphanumeric with underscore
        c = str(col).lower()
        c = re.sub(r"[^\\w]+", "_", c)
        c = re.sub(r"_+", "_", c).strip("_")

        if not c:
            c = "unnamed"

        # Deduplicate
        if c in seen:
            seen[c] += 1
            c = f"{{c}}_{{seen[c]}}"
        else:
            seen[c] = 1

        new_cols.append(c)

    df.columns = new_cols
    return df


def infer_and_cast_dtypes(
    df: pd.DataFrame, *, cat_max_ratio: float = 0.2, cat_max_unique: int = 50
) -> pd.DataFrame:
    \"\"\"Infer best-effort dtypes for dataframe columns.\"\"\"
    for col in df.columns:
        # Try converting to numeric first
        try:
            df[col] = pd.to_numeric(df[col])
        except (ValueError, TypeError):
            pass

        # Attempt datetime conversion for object columns that look like dates
        if pd.api.types.is_object_dtype(df[col]) or pd.api.types.is_string_dtype(df[col]):
            try:
                # Only convert if it's not just numbers
                if not df[col].astype(str).str.isnumeric().all():
                    parsed = pd.to_datetime(df[col], errors="coerce", format="mixed")
                    if not parsed.isna().all() and parsed.notna().mean() >= 0.5:
                        df[col] = parsed
            except (ValueError, TypeError):
                pass

    # Use pandas nullable types (Int64, Float64, String, Boolean)
    df = df.convert_dtypes()

    # Convert low-cardinality strings/objects to categories
    for col in df.select_dtypes(include=["string", "object"]).columns:
        n_unique = df[col].nunique()
        n_rows = len(df)
        if n_unique <= cat_max_unique and (n_unique / n_rows) <= cat_max_ratio:
            df[col] = df[col].astype("category")

    return df


def ingest_file(
    input_path: Path,
    *,
    interim_dir: Path = Path("data/interim"),
    dry_run: bool = False,
) -> Path | None:
    \"\"\"Orchestrate the ingestion pipeline.\"\"\"
    df = load_data(input_path)
    df = normalize_columns(df)
    df = infer_and_cast_dtypes(df)

    if dry_run:
        logger.info("Dry run: Schema would be:\\n%s", df.dtypes)
        return None

    interim_dir.mkdir(parents=True, exist_ok=True)
    
    parquet_path = interim_dir / f"{{input_path.stem}}_clean.parquet"
    csv_path = interim_dir / f"{{input_path.stem}}_clean.csv"
    
    df.to_parquet(parquet_path)
    df.to_csv(csv_path, index=False)
    
    logger.info(f"Saved clean data to {{parquet_path}} and {{csv_path}}")
    return parquet_path
"""


def _process_py(project: str) -> str:
    return f"""\
\"\"\"
{project}/process.py
====================

Data cleaning, normalisation, and feature engineering.
\"\"\"
from __future__ import annotations

from pathlib import Path
from typing import Literal, Union

import numpy as np
import pandas as pd

from {project}.utils import get_logger, load_data

logger = get_logger(__name__)


def clean_missing(
    df: pd.DataFrame,
    *,
    strategy: Literal["drop", "median", "mean", "mode", "constant"] = "median",
    constant: Union[float, str, None] = 0,
    min_non_null_ratio: float = 0.5,
) -> pd.DataFrame:
    \"\"\"Handle missing values by dropping sparse columns and imputing the rest.\"\"\"
    # Drop columns with too many missing values
    threshold = int(len(df) * min_non_null_ratio)
    df = df.dropna(axis=1, thresh=threshold)

    # Impute numeric columns
    numeric_cols = df.select_dtypes(include=np.number).columns
    for col in numeric_cols:
        if strategy == "median":
            fill_val = df[col].median()
        elif strategy == "mean":
            fill_val = df[col].mean()
        elif strategy == "mode":
            fill_val = df[col].mode()[0]
        else:
            fill_val = constant
        df[col] = df[col].fillna(fill_val)

    # Impute categorical columns (always mode or constant)
    cat_cols = df.select_dtypes(exclude=np.number).columns
    for col in cat_cols:
        if strategy == "constant":
            fill_val = str(constant)
        else:
            # Default to mode for categorical if not constant
            fill_val = df[col].mode()[0] if not df[col].mode().empty else "unknown"
        df[col] = df[col].fillna(fill_val)

    return df


def encode_for_ml(
    df: pd.DataFrame, *, drop_non_numeric: bool = True
) -> tuple[pd.DataFrame, np.ndarray]:
    \"\"\"Prepare a numeric matrix X for analysis.\"\"\"
    if drop_non_numeric:
        # Simple approach: keep only numeric
        df_encoded = df.select_dtypes(include=np.number).copy()
    else:
        # One-hot encode categoricals
        df_encoded = pd.get_dummies(df, drop_first=True)

    # Ensure we have no remaining NaNs (should be handled by clean_missing, but safety first)
    df_encoded = df_encoded.fillna(0)
    
    return df_encoded, df_encoded.to_numpy()


def process_file(
    input_path: Path,
    *,
    processed_dir: Path = Path("data/processed"),
) -> Path:
    \"\"\"Load interim data, clean, and save processed data.\"\"\"
    logger.info(f"Processing {{input_path}}")
    
    df = load_data(input_path)
    df = clean_missing(df)
    
    processed_dir.mkdir(parents=True, exist_ok=True)
    parquet_path = processed_dir / f"{{input_path.stem}}_processed.parquet"
    csv_path = processed_dir / f"{{input_path.stem}}_processed.csv"
    
    df.to_parquet(parquet_path)
    df.to_csv(csv_path, index=False)
        
    logger.info(f"Saved processed data to {{parquet_path}} and {{csv_path}}")
    return parquet_path
"""


def _analyze_py(project: str) -> str:
    return f"""\
\"\"\"
{project}/analyze.py
====================

Exploratory data analysis, statistics, and model training.
\"\"\"
from __future__ import annotations

import pickle
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from {project}.process import encode_for_ml
from {project}.utils import AnalysisResult, get_logger, load_data

logger = get_logger(__name__)


def run_unsupervised(
    df: pd.DataFrame,
    *,
    n_components: int = 2,
    cluster_k: int = 3,
    random_state: int = 42,
    output_dir: Path = Path("reports/figures"),
) -> AnalysisResult:
    \"\"\"Run PCA and K-Means clustering.\"\"\"
    output_dir.mkdir(parents=True, exist_ok=True)
    artifacts = {{}}

    # 1. Prepare Data
    df_num, X = encode_for_ml(df, drop_non_numeric=True)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 2. PCA
    pca = PCA(n_components=n_components, random_state=random_state)
    X_pca = pca.fit_transform(X_scaled)
    
    loadings = pd.DataFrame(
        pca.components_.T, 
        columns=[f"PC{{i+1}}" for i in range(n_components)], 
        index=df_num.columns
    )

    # 3. Clustering
    kmeans = KMeans(n_clusters=cluster_k, random_state=random_state, n_init="auto")
    labels = kmeans.fit_predict(X_scaled)

    # 4. Correlation
    corr = df_num.corr()

    # 5. Basic Plots (Artifacts)
    # Correlation Heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, cmap="coolwarm", center=0, annot=False)
    plt.title("Correlation Matrix")
    corr_path = output_dir / "corr_heatmap.png"
    plt.savefig(corr_path, dpi=300, bbox_inches="tight")
    plt.close()
    artifacts["corr_heatmap"] = corr_path

    # PCA Scatter
    plt.figure(figsize=(8, 6))
    plt.scatter(X_pca[:, 0], X_pca[:, 1], c=labels, cmap="viridis", alpha=0.6)
    plt.xlabel(f"PC1 ({{pca.explained_variance_ratio_[0]:.1%}} var)")
    plt.ylabel(f"PC2 ({{pca.explained_variance_ratio_[1]:.1%}} var)")
    plt.title("PCA Score Plot")
    pca_path = output_dir / "pca_scatter.png"
    plt.savefig(pca_path, dpi=300, bbox_inches="tight")
    plt.close()
    artifacts["pca_scatter"] = pca_path

    return AnalysisResult(
        pca_components=X_pca,
        pca_loadings=loadings,
        cluster_labels=labels,
        corr=corr,
        artifacts=artifacts,
    )


def analyze_file(
    input_path: Path,
    *,
    output_dir: Path = Path("data/processed"),
) -> Path:
    \"\"\"Run analysis pipeline and save results object.\"\"\"
    logger.info(f"Analyzing {{input_path}}")
    df = load_data(input_path)
    
    result = run_unsupervised(df)
    
    # Save the result object for the visualization step
    output_dir.mkdir(parents=True, exist_ok=True)
    result_path = output_dir / f"{{input_path.stem}}_analysis.pkl"
    with open(result_path, "wb") as f:
        pickle.dump(result, f)
        
    logger.info(f"Analysis saved to {{result_path}}")
    return result_path
"""


def _visualize_py(project: str) -> str:
    return f"""\
\"\"\"
{project}/visualize.py
======================

Figure generation and saving.
\"\"\"
from __future__ import annotations

import pickle
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from {project}.utils import AnalysisResult, get_logger, load_data

logger = get_logger(__name__)


def make_dashboard(
    df: pd.DataFrame,
    analysis: AnalysisResult,
    *,
    output_dir: Path = Path("reports/figures"),
) -> list[Path]:
    \"\"\"Generate a summary dashboard.\"\"\"
    output_dir.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid", context="talk")
    
    # Augment DF with analysis results for plotting
    plot_df = df.copy()
    plot_df["Cluster"] = analysis.cluster_labels.astype(str)
    plot_df["PC1"] = analysis.pca_components[:, 0]
    plot_df["PC2"] = analysis.pca_components[:, 1]

    # 1. Dashboard Figure
    fig = plt.figure(figsize=(18, 10), constrained_layout=True)
    gs = fig.add_gridspec(2, 3)

    # A: PCA Scatter
    ax1 = fig.add_subplot(gs[0, 0])
    sns.scatterplot(data=plot_df, x="PC1", y="PC2", hue="Cluster", ax=ax1, palette="viridis")
    ax1.set_title("PCA Clusters")

    # B: Correlation Heatmap (Small)
    ax2 = fig.add_subplot(gs[0, 1])
    sns.heatmap(analysis.corr, cmap="coolwarm", center=0, cbar=False, ax=ax2)
    ax2.set_title("Feature Correlation")

    # C: Distribution of first 3 numeric features
    numeric_cols = df.select_dtypes(include="number").columns[:3]
    for i, col in enumerate(numeric_cols):
        if i >= 3: break # Limit to 3
        ax = fig.add_subplot(gs[1, i])
        sns.boxplot(data=plot_df, x="Cluster", y=col, ax=ax, palette="viridis")
        ax.set_title(f"{{col}} by Cluster")

    dashboard_path = output_dir / "dashboard_summary.png"
    fig.suptitle("Project Dashboard", fontsize=20)
    fig.savefig(dashboard_path, dpi=300)
    plt.close()
    
    logger.info(f"Dashboard saved to {{dashboard_path}}")
    return [dashboard_path]


def visualize_file(
    data_path: Path,
    analysis_path: Path,
    *,
    output_dir: Path = Path("reports/figures"),
) -> None:
    \"\"\"Load data and analysis results to generate figures.\"\"\"
    logger.info(f"Visualizing {{data_path}}")
    
    df = load_data(data_path)
    
    with open(analysis_path, "rb") as f:
        analysis: AnalysisResult = pickle.load(f)
        
    make_dashboard(df, analysis, output_dir=output_dir)
"""


def _cli_py(project: str, author: str) -> str:
    """Return a full Typer + Rich CLI stub for the scaffolded project."""
    auth = author if author else "[Your name]"
    return f"""\
#!/usr/bin/env python3
\"\"\"
cli.py
======

Command-line interface for **{project}**.
\"\"\"
from __future__ import annotations

import logging
from pathlib import Path

import typer
from rich.console import Console
from rich.logging import RichHandler

# Import pipeline modules
from {project} import analyze, ingest, process, visualize

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True, show_path=False)],
)
logger = logging.getLogger(__name__)
console = Console()
app = typer.Typer(
    name="{project}",
    help="Data Science Pipeline CLI.",
    add_completion=False,
)


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


@app.command()
def ingest_cmd(
    input: Path = typer.Option(..., "--input", "-i", help="Path to raw input file."),
    dry_run: bool = typer.Option(False, "--dry-run", help="Validate only, do not write."),
) -> None:
    \"\"\"Load raw data, validate schema, and save to data/interim/.\"\"\"
    try:
        ingest.ingest_file(input, dry_run=dry_run)
    except Exception:
        logger.exception("Ingestion failed")
        raise typer.Exit(code=1)


@app.command()
def process_cmd(
    input: Path = typer.Option(..., "--input", "-i", help="Path to interim data file."),
) -> None:
    \"\"\"Clean, normalise, and engineer features. Writes to data/processed/.\"\"\"
    try:
        process.process_file(input)
    except Exception:
        logger.exception("Processing failed")
        raise typer.Exit(code=1)


@app.command()
def analyze_cmd(
    input: Path = typer.Option(..., "--input", "-i", help="Path to processed data file."),
) -> None:
    \"\"\"Run EDA, statistics, or model training.\"\"\"
    try:
        analyze.analyze_file(input)
    except Exception:
        logger.exception("Analysis failed")
        raise typer.Exit(code=1)


@app.command()
def visualize_cmd(
    input: Path = typer.Option(..., "--input", "-i", help="Path to processed data file."),
    analysis: Path = typer.Option(
        None, "--analysis", "-a", help="Path to analysis .pkl file (defaults to matching input stem)."
    ),
    output_dir: Path = typer.Option(
        Path("reports/figures"), "--output-dir", "-o", help="Directory for saved figures."
    ),
) -> None:
    \"\"\"Generate and save all project figures.\"\"\"
    try:
        # Default analysis path: data/processed/{{stem}}_analysis.pkl
        if analysis is None:
            analysis = input.parent / f"{{input.stem}}_analysis.pkl"
        
        if not analysis.exists():
            logger.error(f"Analysis file not found: {{analysis}}. Run 'analyze' first.")
            raise typer.Exit(code=1)
            
        visualize.visualize_file(input, analysis, output_dir=output_dir)
    except Exception:
        logger.exception("Visualization failed")
        raise typer.Exit(code=1)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app()
"""


def _pyproject_toml(project: str, description: str, author: str) -> str:
    """Return a pyproject.toml for the scaffolded project (not the tool itself)."""
    safe_name = project.lower().replace(" ", "-").replace("_", "-")
    pkg_name = project.lower().replace("-", "_").replace(" ", "_")
    desc = description if description else f"Data science project: {project}"
    auth = author if author else "Author"
    return f"""\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "{safe_name}"
version = "0.1.0"
description = "{desc}"
authors = [{{name = "{auth}"}}]
requires-python = ">=3.11"
dependencies = [
    "typer>=0.12",
    "rich>=13",
    "pandas>=2",
    "polars>=0.20",
    "numpy>=1.26",
    "matplotlib>=3.8",
    "seaborn>=0.13",
    "plotly>=5.20",
    "scikit-learn>=1.4",
]

[project.optional-dependencies]
dev = [
    "pytest>=8",
    "pytest-cov",
    "ruff>=0.4",
    "ipykernel",
]

[project.scripts]
{safe_name} = "cli:app"

[tool.hatch.build.targets.wheel]
packages = [
    "{pkg_name}",
]

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

# uv
.python-version
uv.lock

# Data (raw/interim should not be committed unless tiny)
data/raw/*
data/interim/*
data/processed/*
!data/raw/.gitkeep
!data/interim/.gitkeep
!data/processed/.gitkeep

# Reports / outputs
reports/figures/*
!reports/figures/.gitkeep
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
    desc = (
        description if description else "[Add a one-paragraph project description here]"
    )
    auth = author if author else "[Your name]"
    safe = project.lower().replace(" ", "-").replace("_", "-")
    return f"""\
# {project}

{desc}

## Setup

```bash
# With uv (recommended)
uv sync

# Or with pip
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install -e ".[dev]"
```

## Usage

```bash
python cli.py --help
python cli.py ingest   --input data/raw/<file>
python cli.py process  --input data/interim/<file>
python cli.py analyze  --input data/processed/<file>
python cli.py visualize --input data/processed/<file>
```

## Project Structure

```
{project}/
├── AGENTS.md           # AI briefing — paste at start of every session
├── CONTEXT.md          # Living project state — update after every session
├── dev-notes.md        # Prompt log, decisions, AI gotchas
├── cli.py              # Pipeline CLI entry point
├── data/
│   ├── raw/            # Source data — never modify
│   ├── interim/        # Mid-processing artifacts
│   └── processed/      # Final clean datasets
├── {project}/
│   ├── ingest.py       # Data loading & schema validation
│   ├── process.py      # Cleaning & feature engineering
│   ├── analyze.py      # EDA, statistics, modelling
│   └── visualize.py    # Figure generation
├── notebooks/          # Exploration notebooks (not production)
├── reports/
│   └── figures/        # Saved plots (PNG + HTML)
├── tests/              # pytest suite
├── pyproject.toml
└── .gitignore
```

## AI Workflow

| File | When to update |
|---|---|
| `AGENTS.md` | Once — customise for your stack and rules |
| `CONTEXT.md` | End of every session — state, blockers, next steps |
| `dev-notes.md` | Continuously — log working prompts and decisions |

## Author
{auth}

## License
MIT
"""


def _test_pipeline_py(project: str) -> str:
    return f"""\
\"\"\"
tests/test_pipeline.py
======================

Tests for the core data pipeline modules.
\"\"\"
import numpy as np
import pandas as pd
import pytest
from {project} import ingest, process, analyze


@pytest.fixture
def sample_df():
    \"\"\"Create a messy dataframe for testing.\"\"\"
    return pd.DataFrame({{
        "ID Column": [1, 2, 3, 4, 5],
        "  Messy  Name! ": ["A", "B", "A", "B", "C"],
        "Date Str": ["2023-01-01", "2023-01-02", "not a date", "2023-01-04", "2023-01-05"],
        "Numbers": ["1.1", "2.2", "3.3", np.nan, "5.5"],
        "Missing": [1, None, None, None, None],  # Mostly missing
    }})


def test_normalize_columns(sample_df):
    df = ingest.normalize_columns(sample_df)
    expected = ["id_column", "messy_name", "date_str", "numbers", "missing"]
    assert list(df.columns) == expected


def test_infer_dtypes(sample_df):
    df = ingest.normalize_columns(sample_df)
    df = ingest.infer_and_cast_dtypes(df, cat_max_ratio=1.0)
    
    # Check numeric conversion
    assert pd.api.types.is_float_dtype(df["numbers"])
    
    # Check datetime conversion (invalid date should be NaT)
    assert pd.api.types.is_datetime64_any_dtype(df["date_str"])
    assert pd.isna(df.loc[2, "date_str"])
    
    # Check category conversion (low cardinality)
    assert isinstance(df["messy_name"].dtype, pd.CategoricalDtype)


def test_clean_missing(sample_df):
    df = ingest.normalize_columns(sample_df)
    df = ingest.infer_and_cast_dtypes(df)
    
    # "missing" column has 3/5 NaNs (60%), default threshold is 0.5 (50% non-null required)
    # So it should be dropped (only 40% non-null)
    df_clean = process.clean_missing(df, min_non_null_ratio=0.5, strategy="mean")
    
    assert "missing" not in df_clean.columns
    assert "numbers" in df_clean.columns
    assert not df_clean["numbers"].isna().any()  # Should be imputed


def test_analysis_shape(sample_df):
    # Setup clean data
    df = ingest.normalize_columns(sample_df)
    df = ingest.infer_and_cast_dtypes(df)
    df = process.clean_missing(df)
    
    # Run analysis
    result = analyze.run_unsupervised(df, n_components=2, cluster_k=2)
    
    # Check shapes
    n_rows = len(df)
    assert result.pca_components.shape == (n_rows, 2)
    assert len(result.cluster_labels) == n_rows
    
    # Check artifacts
    assert "corr_heatmap" in result.artifacts
    assert "pca_scatter" in result.artifacts
"""



# ---------------------------------------------------------------------------
# Manifest & directory layout
# ---------------------------------------------------------------------------

DIRS: list[str] = [
    "data/raw",
    "data/interim",
    "data/processed",
    "{pkg_name}",
    "notebooks",
    "reports/figures",
    "tests",
]


def build_manifest(
    root: Path,
    project: str,
    description: str,
    author: str,
) -> list[tuple[Path, str]]:
    """Return a list of ``(path, content)`` pairs for all files to create.

    Args:
        root: Absolute path to the project root directory.
        project: Project name (used in headers and identifiers).
        description: One-line project description.
        author: Author name for file headers.

    Returns:
        Ordered list of (path, content) tuples ready to be written to disk.
    """
    pkg_name = project.lower().replace("-", "_").replace(" ", "_")
    src_dir = root / pkg_name
    tests = root / "tests"

    manifest: list[tuple[Path, str]] = [
        # AI context files
        (root / "AGENTS.md", _agents_md(project, description, author)),
        (root / "CONTEXT.md", _context_md(project, description)),
        (root / "dev-notes.md", _dev_notes_md(project)),
        # Project meta
        (root / "README.md", _readme(project, description, author)),
        (root / "pyproject.toml", _pyproject_toml(project, description, author)),
        (root / ".gitignore", _gitignore()),
        # CLI
        (root / "cli.py", _cli_py(pkg_name, author)),
        # src package
        (src_dir / "__init__.py", f'"""Source package for the {project} project."""\n'),
        (src_dir / "utils.py", _utils_py(pkg_name)),
        (src_dir / "ingest.py", _ingest_py(pkg_name)),
        (src_dir / "process.py", _process_py(pkg_name)),
        (src_dir / "analyze.py", _analyze_py(pkg_name)),
        (src_dir / "visualize.py", _visualize_py(pkg_name)),
        # tests
        (tests / "__init__.py", f'"""Tests for the {project} project."""\n'),
        (tests / "test_pipeline.py", _test_pipeline_py(pkg_name)),
    ]
    return manifest


# ---------------------------------------------------------------------------
# CLI command
# ---------------------------------------------------------------------------


@app.command()
def scaffold(
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
        Path("."), "--output", "-o", help="Parent directory for the new project."
    ),
    force: bool = typer.Option(
        False, "--force", "-f", help="Overwrite existing files without prompting."
    ),
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        callback=_version_callback,
        is_eager=True,
        help="Show version and exit.",
    ),
) -> None:
    """Scaffold a new DS/ML project with AI context files and Python stubs."""
    root = output_dir.expanduser().resolve() / project_name

    # --- Header banner ---
    console.print()
    console.print(
        Panel.fit(
            f"[bold white]ds-scaffold[/]  v{__version__}  ·  DS/ML Project Scaffolder\n"
            f"[muted]Target:[/] [bold cyan]{root}[/]",
            border_style="dark_blue",
            padding=(0, 2),
        )
    )
    console.print()

    # --- Guard: existing directory ---
    if root.exists() and not force:
        console.print(f"[warning]⚠  Directory already exists:[/] {root}")
        if not typer.confirm("Overwrite existing files?", default=False):
            console.print("[muted]Aborted.[/]")
            raise typer.Exit(0)

    # ── Step 1: directories ──────────────────────────────────────────────────
    console.print("[info]❶  Creating directory structure…[/]")
    pkg_name = project_name.lower().replace("-", "_").replace(" ", "_")
    dirs_to_create = [root / d.replace("{pkg_name}", pkg_name) for d in DIRS]

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=32),
        TaskProgressColumn(),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task("Directories", total=len(dirs_to_create))
        for d in dirs_to_create:
            d.mkdir(parents=True, exist_ok=True)
            (d / ".gitkeep").touch()
            progress.advance(task)

    console.print(f"   [success]✔[/]  {len(dirs_to_create)} directories created\n")

    # ── Step 2: files ────────────────────────────────────────────────────────
    console.print("[info]❷  Writing files…[/]")
    manifest = build_manifest(root, project_name, description, author)
    created, skipped = 0, 0

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description:<42}"),
        BarColumn(bar_width=32),
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
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
                created += 1
            progress.advance(task)

    console.print(
        f"   [success]✔[/]  {created} files written"
        + (f",  {skipped} skipped (use --force to overwrite)" if skipped else "")
        + "\n"
    )

    # ── Step 3: summary ──────────────────────────────────────────────────────
    console.print("[info]❸  Project summary[/]\n")

    table = Table(
        show_header=True,
        header_style="header",
        border_style="bright_black",
        expand=False,
    )
    table.add_column("Category", style="bold cyan", min_width=16)
    table.add_column("Path", style="white", min_width=22)
    table.add_column("Purpose", style="dim white")

    rows = [
        ("AI Briefing", "AGENTS.md", "Paste at the start of every AI session"),
        ("AI State", "CONTEXT.md", "Update at the end of every session"),
        ("Prompt Log", "dev-notes.md", "Working prompts, decisions, AI gotchas"),
        ("CLI", "cli.py", "Pipeline entry point (ingest/process/analyze/viz)"),
        ("Ingest", f"{pkg_name}/ingest.py", "Raw data loading & schema validation"),
        ("Process", f"{pkg_name}/process.py", "Cleaning, normalisation, feature engineering"),
        ("Analyze", f"{pkg_name}/analyze.py", "EDA, stats, model training"),
        ("Visualize", f"{pkg_name}/visualize.py", "Figure generation & saving"),
        ("Tests", "tests/test_pipeline.py", f"pytest suite for {project_name} pipeline"),
        ("Config", "pyproject.toml", "Dependencies, scripts, ruff & pytest config"),
    ]
    for category, path, purpose in rows:
        table.add_row(category, path, purpose)

    console.print(table)
    console.print()

    # ── Next steps ───────────────────────────────────────────────────────────
    console.print(
        Panel(
            "[bold white]Next steps[/]\n\n"
            f"  [cyan]cd {root}[/]\n\n"
            "  [dim]# With uv (recommended)[/dim]\n"
            "  [cyan]uv sync[/]\n\n"
            "  [dim]# Or with pip[/dim]\n"
            "  [cyan]python -m venv .venv && source .venv/bin/activate[/]\n"
            "  [cyan]pip install -e '.[dev]'[/]\n\n"
            "  [dim]Then open [/dim][bold white]AGENTS.md[/][dim] and fill in your project brief.[/]\n"
            "  [cyan]git init && git add . && git commit -m 'chore: initial scaffold'[/]",
            border_style="green",
            padding=(0, 2),
        )
    )
    console.print()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    """Entry point registered by pyproject.toml for `ds-scaffold`."""
    app()


if __name__ == "__main__":
    main()
