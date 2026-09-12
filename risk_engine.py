
def calculate_risk(
    exposure: float,
    vulnerability: float,
    adaptive_capacity: float,
    sensitivity: float,
    criticality: float,
    scenario: str = "Moderate",
    horizon: str = "Mid Century"
) -> dict:
    """Calculates overall composite risk, climate stress, resilience, and gap using dynamic input parameters."""
    # Scenario multipliers
    scenario_weights = {"Low": 0.85, "Moderate": 1.0, "High": 1.25}
    horizon_weights = {"Near Term": 0.9, "Mid Century": 1.05, "Long Term": 1.2}

    s_mult = scenario_weights.get(scenario, 1.0)
    h_mult = horizon_weights.get(horizon, 1.0)

    # Core proxy index calculations
    base_vulnerability = (vulnerability * 0.4) + (sensitivity * 0.4) + (criticality * 0.2)
    adjusted_exposure = exposure * s_mult * h_mult
    
    climate_stress = min(100.0, adjusted_exposure * 0.6 + base_vulnerability * 0.4)
    resilience = min(100.0, adaptive_capacity * 0.8 + (100.0 - base_vulnerability) * 0.2)
    
    # Composite CHRI-style risk assessment proxy formula
    raw_risk = (adjusted_exposure * 0.3) + (base_vulnerability * 0.4) + ((100.0 - adaptive_capacity) * 0.3)
    overall_risk = min(100.0, max(0.0, raw_risk))

    risk_gap = max(0.0, overall_risk - resilience)

    if overall_risk < 40.0:
        category = "Low"
        priority = "Standard Monitoring"
    elif overall_risk < 70.0:
        category = "Moderate"
        priority = "Targeted Intervention"
    else:
        category = "High"
        priority = "Immediate Climate Adaptation"

    return {
        "overall_risk": round(overall_risk, 2),
        "climate_stress": round(climate_stress, 2),
        "resilience": round(resilience, 2),
        "risk_gap": round(risk_gap, 2),
        "risk_category": category,
        "priority": priority,
        "exposure": round(exposure, 2),
        "vulnerability": round(vulnerability, 2),
        "sensitivity": round(sensitivity, 2),
        "adaptive_capacity": round(adaptive_capacity, 2),
        "criticality": round(criticality, 2),
        "methodology": "AquaGuard screening proxy calculation (Non-regulatory)"
    }
