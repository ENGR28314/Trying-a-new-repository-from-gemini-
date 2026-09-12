
import pandas as pd
import numpy as np

def validate_uploaded_dataframe(df: pd.DataFrame) -> dict:
    """Validates uploaded user datasets for structure, missing records, and numeric features."""
    results = {
        "is_valid": True,
        "rows": len(df),
        "columns": len(df.columns),
        "missing_cells": int(df.isnull().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "numeric_cols": list(df.select_dtypes(include=[np.number]).columns),
        "categorical_cols": list(df.select_dtypes(exclude=[np.number]).columns),
        "warnings": []
    }

    if results["rows"] == 0:
        results["is_valid"] = False
        results["warnings"].append("Dataset contains 0 rows.")

    if len(results["numeric_cols"]) == 0:
        results["warnings"].append("No numeric environmental variables detected.")

    if results["missing_cells"] > 0:
        results["warnings"].append(f"Found {results['missing_cells']} missing values across the dataset.")

    if results["duplicate_rows"] > 0:
        results["warnings"].append(f"Found {results['duplicate_rows']} exact duplicate rows.")

    return results
