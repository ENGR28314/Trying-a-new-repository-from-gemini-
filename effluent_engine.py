
def analyze_effluent_discharge(bod: float, cod: float, discharge_flow_m3_day: float) -> dict:
    """Evaluates industrial and municipal wastewater effluent risks."""
    bod_risk = min(100.0, (bod / 30.0) * 50.0)
    cod_risk = min(100.0, (cod / 100.0) * 50.0)
    
    composite_risk = round((bod_risk + cod_risk) / 2.0, 2)
    daily_bod_load_kg = round((bod * discharge_flow_m3_day) / 1000.0, 2)
    
    return {
        "effluent_risk_score": composite_risk,
        "daily_bod_load_kg": daily_bod_load_kg,
        "discharge_volume_m3": discharge_flow_m3_day,
        "compliance_status": "Compliant" if composite_risk < 50.0 else "Non-Compliant"
    }
