"""
tests/test_pipeline.py
======================

Tests for the core data pipeline modules.
"""
import numpy as np
import pandas as pd
import pytest
from src import ingest, process, analyze


@pytest.fixture
def sample_df():
    """Create a messy dataframe for testing."""
    return pd.DataFrame({
        "ID Column": [1, 2, 3, 4, 5],
        "  Messy  Name! ": ["A", "B", "A", "B", "C"],
        "Date Str": ["2023-01-01", "2023-01-02", "not a date", "2023-01-04", "2023-01-05"],
        "Numbers": ["1.1", "2.2", "3.3", "NaN", "5.5"],
        "Missing": [1, None, None, None, 5],  # Mostly missing
    })


def test_normalize_columns(sample_df):
    df = ingest.normalize_columns(sample_df)
    expected = ["id_column", "messy_name", "date_str", "numbers", "missing"]
    assert list(df.columns) == expected


def test_infer_dtypes(sample_df):
    df = ingest.normalize_columns(sample_df)
    df = ingest.infer_and_cast_dtypes(df)
    
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
    # Wait, min_non_null_ratio=0.5 means we need 50% data. 2/5 is 40%. So drop.
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