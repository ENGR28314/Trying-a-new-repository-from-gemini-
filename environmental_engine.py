
import pandas as pd
import numpy as np

DEFAULT_THRESHOLDS = {
    "temperature": {"threshold": 35.0, "unit": "°C"},
    "rainfall": {"threshold": 200.0, "unit": "mm/mo"},
    "pm25": {"threshold": 35.0, "unit": "µg/m³"},
    "pm10": {"threshold": 50.0, "unit": "µg/m³"},
    "no2": {"threshold": 40.0, "unit": "µg/m³"},
    "bod": {"threshold": 5.0, "unit": "mg/L"},
    "cod": {"threshold": 10.0, "unit": "mg/L"},
    "tds": {"threshold": 500.0, "unit": "mg/L"}
}

def analyze_environmental_dataframe(df: pd.DataFrame) -> dict:
    """Normalizes uploaded environmental records into standard risk indices."""
    summary = []
    total_score = 0.0
    count = 0

    numeric_df = df.select_dtypes(include=[np.number])
    
    for col in numeric_df.columns:
        mean_val = float(numeric_df[col].mean())
        col_lower = col.lower()
        
        # Match threshold
        ref_thresh = 100.0
        unit = "units"
        for key, val in DEFAULT_THRESHOLDS.items():
            if key in col_lower:
                ref_thresh = val["threshold"]
                unit = val["unit"]
                break

        norm_score = min(100.0, (mean_val / ref_thresh) * 50.0) if ref_thresh > 0 else 50.0
        
        category = "Low" if norm_score < 40 else ("Moderate" if norm_score < 70 else "High")
        
        summary.append({
            "variable": col,
            "observed_mean": round(mean_val, 2),
            "threshold": ref_thresh,
            "unit": unit,
            "normalized_score": round(norm_score, 2),
            "risk_category": category
        })
        
        total_score += norm_score
        count += 1

    avg_env_risk = round(total_score / count, 2) if count > 0 else 30.0

    return {
        "environmental_risk_score": avg_env_risk,
        "variables_analyzed": count,
        "details": pd.DataFrame(summary)
    }
