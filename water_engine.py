
def analyze_water_quality(ph: float, tds: float, dissolved_oxygen: float) -> dict:
    """Analyzes physical-chemical water parameters."""
    ph_score = 10.0 if 6.5 <= ph <= 8.5 else 75.0
    tds_score = min(100.0, (tds / 1000.0) * 50.0)
    do_score = min(100.0, max(0.0, (8.0 - dissolved_oxygen) * 12.5))
    
    composite = round((ph_score + tds_score + do_score) / 3.0, 2)
    
    return {
        "water_quality_risk_score": composite,
        "status": "Good" if composite < 40 else ("Stressed" if composite < 70 else "Critical"),
        "ph_status": "Normal" if ph_score == 10.0 else "Out of Range",
        "tds_mg_l": tds,
        "dissolved_oxygen_mg_l": dissolved_oxygen
    }
