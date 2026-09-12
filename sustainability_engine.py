
import pandas as pd

def get_sustainability_mappings() -> pd.DataFrame:
    """Maps environmental action vectors to ESG, SDG, MDG, and ISO frameworks."""
    data = [
        {
            "Domain": "Environmental",
            "ESG Focus Area": "Climate Change & Carbon",
            "Relevant SDG": "SDG 13: Climate Action",
            "Legacy MDG Alignment": "MDG 7: Environmental Sustainability",
            "ISO Framework": "ISO 14064 (GHG Quantification)"
        },
        {
            "Domain": "Environmental",
            "ESG Focus Area": "Water & Effluent Management",
            "Relevant SDG": "SDG 6: Clean Water and Sanitation",
            "Legacy MDG Alignment": "MDG 7: Safe Drinking Water Access",
            "ISO Framework": "ISO 14001 (Environmental Management)"
        },
        {
            "Domain": "Social",
            "ESG Focus Area": "Community Resilience & Health",
            "Relevant SDG": "SDG 11: Sustainable Cities",
            "Legacy MDG Alignment": "MDG 3: Vulnerable Populations",
            "ISO Framework": "ISO 31000 (Risk Management)"
        },
        {
            "Domain": "Governance",
            "ESG Focus Area": "Energy Efficiency & Systems",
            "Relevant SDG": "SDG 7: Clean Energy",
            "Legacy MDG Alignment": "MDG 7: Global Partnerships",
            "ISO Framework": "ISO 50001 (Energy Management)"
        }
    ]
    return pd.DataFrame(data)
