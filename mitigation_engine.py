
import pandas as pd

def generate_mitigation_plan(risk_category: str, top_hazard: str) -> pd.DataFrame:
    """Generates targeted action items aligned with risk profile and hazards."""
    plan = [
        {
            "Risk Driver": top_hazard,
            "Sector": "Infrastructure / Water",
            "Mitigation Measure": f"Install high-capacity stormwater drainage and {top_hazard.lower()} retention basins.",
            "Adaptation Measure": "Implement nature-based coastal and riverine buffer zones.",
            "Priority": "High" if risk_category == "High" else "Medium",
            "KPI": "Reduction in urban inundation frequency (30% by 2028)"
        },
        {
            "Risk Driver": "GHG & Carbon",
            "Sector": "Energy",
            "Mitigation Measure": "Transition facility power to microgrid solar PV and energy storage system.",
            "Adaptation Measure": "Deploy dynamic smart-grid load controls.",
            "Priority": "Medium",
            "KPI": "tCO2e reduction per annum (Target 25%)"
        },
        {
            "Risk Driver": "Water Quality & Effluent",
            "Sector": "Industry / Waste",
            "Mitigation Measure": "Construct advanced biological effluent treatment plant (ETP).",
            "Adaptation Measure": "Closed-loop industrial water recycling system.",
            "Priority": "High",
            "KPI": "Zero liquid discharge (ZLD) compliance index"
        }
    ]
    return pd.DataFrame(plan)
