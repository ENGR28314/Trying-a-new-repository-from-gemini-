
import pandas as pd
import io

def generate_consolidated_report(
    project_info: dict,
    risk_dict: dict,
    hazards_dict: dict,
    ghg_dict: dict
) -> bytes:
    """Generates an Excel workbook summarizing the decision support assessment."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        pd.DataFrame([project_info]).to_excel(writer, sheet_name='Project Metadata', index=False)
        pd.DataFrame([risk_dict]).to_excel(writer, sheet_name='Risk Summary', index=False)
        
        hazards_df = pd.DataFrame([{"Hazard": k, "Score": v["score"], "Category": v["category"]} for k, v in hazards_dict.items()])
        hazards_df.to_excel(writer, sheet_name='Hazard Screening', index=False)
        
        pd.DataFrame([ghg_dict]).to_excel(writer, sheet_name='GHG Footprint', index=False)
        
    return output.getvalue()
