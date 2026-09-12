
import pandas as pd

SECTORS = [
    "Agriculture", "Water", "Energy", "Health", "Transportation",
    "Infrastructure", "Urban Development", "Industry", "Tourism", "Forestry"
]

def evaluate_sector_risks(overall_risk: float, hazard_scores: dict) -> pd.DataFrame:
    """Calculates sector-specific vulnerabilities based on hazard and overall risk factors."""
    sector_data = []
    
    top_hazard = max(hazard_scores, key=lambda k: hazard_scores[k]["score"]) if hazard_scores else "Flood"
    
    for idx, s in enumerate(SECTORS):
        # Vary sector multipliers realistically
        multiplier = 0.8 + ((idx % 4) * 0.1)
        s_score = min(100.0, round(overall_risk * multiplier, 2))
        category = "Low" if s_score < 40 else ("Moderate" if s_score < 70 else "High")
        
        sector_data.append({
            "Sector": s,
            "Sector Risk Score": s_score,
            "Risk Category": category,
            "Top Hazard Driver": top_hazard
        })
        
    return pd.DataFrame(sector_data)
