
def get_carbon_footprint_summary(ghg_data: dict, population: int = 100000) -> dict:
    """Derives carbon footprint indicators and per-capita intensity."""
    total = ghg_data.get("total_tco2e", 0.0)
    per_capita = round((total * 1000.0) / max(population, 1), 3) # kg CO2e per capita
    
    return {
        "total_emissions_tco2e": total,
        "per_capita_kg_co2e": per_capita,
        "reduction_target_2030": round(total * 0.45, 2), # 45% reduction target
        "largest_emitter": ghg_data.get("primary_source", "Scope 1")
    }
