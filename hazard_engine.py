
def calculate_flood_risk(exposure, vulnerability, adaptive_capacity, scenario_factor):
    return min(100.0, ((exposure * 0.5) + (vulnerability * 0.5) - (adaptive_capacity * 0.2)) * scenario_factor)

def calculate_drought_risk(exposure, vulnerability, adaptive_capacity, scenario_factor):
    return min(100.0, ((exposure * 0.4) + (vulnerability * 0.6) - (adaptive_capacity * 0.3)) * scenario_factor)

def calculate_heat_risk(exposure, vulnerability, adaptive_capacity, scenario_factor):
    return min(100.0, ((exposure * 0.6) + (vulnerability * 0.4) - (adaptive_capacity * 0.2)) * scenario_factor)

def calculate_wildfire_risk(exposure, vulnerability, adaptive_capacity, scenario_factor):
    return min(100.0, ((exposure * 0.5) + (vulnerability * 0.3) - (adaptive_capacity * 0.1)) * scenario_factor)

HAZARD_ENGINES = {
    "Flood": calculate_flood_risk,
    "Drought": calculate_drought_risk,
    "Extreme Heat": calculate_heat_risk,
    "Wildfire": calculate_wildfire_risk
}

def evaluate_all_hazards(exposure: float, vulnerability: float, adaptive_capacity: float, scenario: str = "Moderate") -> dict:
    scenario_map = {"Low": 0.85, "Moderate": 1.0, "High": 1.25}
    factor = scenario_map.get(scenario, 1.0)
    
    results = {}
    for h_name, h_func in HAZARD_ENGINES.items():
        score = round(max(0.0, h_func(exposure, vulnerability, adaptive_capacity, factor)), 2)
        category = "Low" if score < 40 else ("Moderate" if score < 70 else "High")
        results[h_name] = {"score": score, "category": category}

    return results
