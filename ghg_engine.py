
def calculate_ghg_emissions(
    fuel_liters: float = 0.0,
    elec_kwh: float = 0.0,
    waste_tons: float = 0.0,
    scope1_ef: float = 2.68,  # kg CO2e / L diesel
    scope2_ef: float = 0.5,   # kg CO2e / kWh grid
    scope3_ef: float = 450.0  # kg CO2e / ton waste
) -> dict:
    """Calculates Scope 1, Scope 2, and Scope 3 greenhouse gas emissions."""
    s1_tco2e = (fuel_liters * scope1_ef) / 1000.0
    s2_tco2e = (elec_kwh * scope2_ef) / 1000.0
    s3_tco2e = (waste_tons * scope3_ef) / 1000.0

    total = round(s1_tco2e + s2_tco2e + s3_tco2e, 2)

    return {
        "scope1_tco2e": round(s1_tco2e, 2),
        "scope2_tco2e": round(s2_tco2e, 2),
        "scope3_tco2e": round(s3_tco2e, 2),
        "total_tco2e": total,
        "primary_source": "Scope 1" if s1_tco2e >= max(s2_tco2e, s3_tco2e) else ("Scope 2" if s2_tco2e >= s3_tco2e else "Scope 3")
    }
