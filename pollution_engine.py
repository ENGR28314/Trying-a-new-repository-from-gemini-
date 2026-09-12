
import pandas as pd

def analyze_air_pollution(pm25: float, pm10: float, no2: float, so2: float) -> pd.DataFrame:
    """Evaluates air quality variables against international safety reference values."""
    metrics = [
        {"Pollutant": "PM2.5", "Observed": pm25, "Threshold": 35.0, "Unit": "µg/m³"},
        {"Pollutant": "PM10", "Observed": pm10, "Threshold": 50.0, "Unit": "µg/m³"},
        {"Pollutant": "NO2", "Observed": no2, "Threshold": 40.0, "Unit": "µg/m³"},
        {"Pollutant": "SO2", "Observed": so2, "Threshold": 20.0, "Unit": "µg/m³"},
    ]
    
    for m in metrics:
        ratio = m["Observed"] / m["Threshold"] if m["Threshold"] > 0 else 1.0
        m["Risk Score"] = round(min(100.0, ratio * 50.0), 2)
        m["Risk Category"] = "Low" if m["Risk Score"] < 40 else ("Moderate" if m["Risk Score"] < 70 else "High")
        
    return pd.DataFrame(metrics)
