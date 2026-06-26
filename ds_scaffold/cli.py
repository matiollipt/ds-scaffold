#!/usr/bin/env python3
"""
cli.py
======

Command-line interface for the project.
"""
from __future__ import annotations

import logging
from pathlib import Path

import typer
from rich.console import Console
from rich.logging import RichHandler

# Import pipeline modules
from src import analyze, ingest, process, visualize

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True, show_path=False)],
)
logger = logging.getLogger(__name__)
console = Console()
app = typer.Typer(
    name="ds-pipeline",
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
    """Load raw data, validate schema, and save to data/interim/."""
    try:
        ingest.ingest_file(input, dry_run=dry_run)
    except Exception as e:
        logger.exception("Ingestion failed")
        raise typer.Exit(code=1)


@app.command()
def process_cmd(
    input: Path = typer.Option(..., "--input", "-i", help="Path to interim data file."),
) -> None:
    """Clean, normalise, and engineer features. Writes to data/processed/."""
    try:
        process.process_file(input)
    except Exception as e:
        logger.exception("Processing failed")
        raise typer.Exit(code=1)


@app.command()
def analyze_cmd(
    input: Path = typer.Option(..., "--input", "-i", help="Path to processed data file."),
) -> None:
    """Run EDA, statistics, or model training."""
    try:
        analyze.analyze_file(input)
    except Exception as e:
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
    """Generate and save all project figures."""
    try:
        # Default analysis path: data/processed/{stem}_analysis.pkl
        if analysis is None:
            analysis = input.parent / f"{input.stem}_analysis.pkl"
        
        if not analysis.exists():
            logger.error(f"Analysis file not found: {analysis}. Run 'analyze' first.")
            raise typer.Exit(code=1)
            
        visualize.visualize_file(input, analysis, output_dir=output_dir)
    except Exception as e:
        logger.exception("Visualization failed")
        raise typer.Exit(code=1)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app()