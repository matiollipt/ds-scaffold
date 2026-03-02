# AidBio ds-scaffold: Standardized Data Science Project Structure

AidBio `ds-scaffold` is a simple, smart tool that creates a standardized folder structure for modern data science projects. It sets up directories for data, notebooks, scripts, and documentation, along with template files—including AI-specific context files—to kickstart your workflow.

## Installation

### From GitHub
To install the tool directly from the repository using `uv`:

```bash
uv tool install git+https://github.com/AidBio/ds-scaffold.git
```

### Local Development
To install the tool from a local clone:

```bash
uv tool install --editable .
```

## Usage

Once installed, you can run `ds-scaffold` from any directory:

```bash
ds-scaffold my-new-project
```

### Options

- `--author`, `-a`: Author name for file headers.
- `--desc`, `-d`: One-line project description.
- `--output`, `-o`: Parent directory for the project (default: current directory).
- `--force`, `-f`: Overwrite existing files without prompting.

## Project Structure

This tool generates a standardized folder structure for data science projects:

```
my-new-project/
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
