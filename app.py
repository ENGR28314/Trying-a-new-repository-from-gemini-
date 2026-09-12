
import streamlit as st
import pandas as pd
import plotly.express as px
import pycountry

from db import get_cached_engine
from data_validation import validate_uploaded_dataframe
from environmental_engine import analyze_environmental_dataframe
from hazard_engine import evaluate_all_hazards
from sector_engine import evaluate_sector_risks
from ghg_engine import calculate_ghg_emissions
from carbon_engine import get_carbon_footprint_summary
from pollution_engine import analyze_air_pollution
from water_engine import analyze_water_quality
from effluent_engine import analyze_effluent_discharge
from mitigation_engine import generate_mitigation_plan
from sustainability_engine import get_sustainability_mappings
from geo_engine import load_cities_from_db, build_world_map
from geoai_ui import render_geoai_dashboard
from report_engine import generate_consolidated_report

# Streamlit Page Setup
st.set_page_config(
    page_title="AquaGuard AI7 — Decision Support Platform",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-Tech Cyber-Environmental CSS Styling
st.markdown("""
<style>
    .stApp {
        background-color: #0A192F;
        color: #E6F1FF;
    }
    .metric-card {
        background: linear-gradient(135deg, #112240 0%, #1D3557 100%);
        border: 1px solid #64FFDA;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    .metric-value {
        font-size: 28px;
        font-weight: bold;
        color: #00E5FF;
    }
    .metric-label {
        font-size: 13px;
        color: #8892B0;
        text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)

# Database connectivity check
engine, db_connected = get_cached_engine()

# Global City Data Setup
cities_df, using_db = load_cities_from_db()

# Sidebar: Project Setup
st.sidebar.title("🌍 Project Setup")

if using_db:
    st.sidebar.success("🟢 PostgreSQL / PostGIS Connected")
else:
    st.sidebar.warning("⚠️ Local Fallback Mode (PostgreSQL Offline)")

project_name = st.sidebar.text_input("Project Name", "AquaGuard Baseline Project")

# Dynamic Country Selection
all_countries = sorted(list(set(cities_df["country"].unique()).union({"Pakistan", "United States", "United Kingdom", "Japan", "Egypt", "Brazil", "Australia", "India"})))
selected_country = st.sidebar.selectbox("Country", all_countries, index=0)

# Filter Cities by Country
country_cities = cities_df[cities_df["country"] == selected_country]
if not country_cities.empty:
    city_names = country_cities["name"].tolist()
else:
    city_names = ["Capital City"]
ai
selected_city = st.sidebar.selectbox("City", city_names)

# Get coordinates
selected_city_row = country_cities[country_cities["name"] == selected_city]
if not selected_city_row.empty:
    lat = float(selected_city_row.iloc[0]["latitude"])
    lon = float(selected_city_row.iloc[0]["longitude"])
    pop = int(selected_city_row.iloc[0].get("population", 100000))
else:
    lat, lon, pop = 24.8607, 67.0011, 500000

climate_division = st.sidebar.text_input("Climate Division", "Division-1 Coastal / Urban")
climate_scenario = st.sidebar.selectbox("Climate Scenario", ["Low", "Moderate", "High"], index=1)
scenario_horizon = st.sidebar.selectbox("Scenario Horizon", ["Near Term", "Mid Century", "Long Term"], index=1)

st.sidebar.markdown("---")
st.sidebar.title("🎛️ Risk Inputs (0-100)")
exposure = st.sidebar.slider("Exposure", 0.0, 100.0, 65.0)
vulnerability = st.sidebar.slider("Population Vulnerability", 0.0, 100.0, 58.0)
sensitivity = st.sidebar.slider("Sensitivity", 0.0, 100.0, 60.0)
adaptive_capacity = st.sidebar.slider("Adaptive Capacity", 0.0, 100.0, 42.0)
criticality = st.sidebar.slider("Asset Criticality", 0.0, 100.0, 70.0)

# Execute Core Risk Engine
risk_results = calculate_risk(
    exposure, vulnerability, adaptive_capacity, sensitivity, criticality,
    scenario=climate_scenario, horizon=scenario_horizon
)

# Execute Hazard Engine
hazards_data = evaluate_all_hazards(exposure, vulnerability, adaptive_capacity, scenario=climate_scenario)

# Title Banner
st.title("🌍 AquaGuard AI7 — Decision Support Platform")
st.markdown(f"**Project:** {project_name} | **Location:** {selected_city}, {selected_country} (`{lat:.4f}, {lon:.4f}`) | **Scenario:** {climate_scenario} ({scenario_horizon})")

# Top KPI Summary Cards
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
with kpi1:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Overall Risk Score</div><div class="metric-value">{risk_results["overall_risk"]}</div></div>', unsafe_allow_html=True)
with kpi2:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Risk Category</div><div class="metric-value">{risk_results["risk_category"]}</div></div>', unsafe_allow_html=True)
with kpi3:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Climate Stress</div><div class="metric-value">{risk_results["climate_stress"]}</div></div>', unsafe_allow_html=True)
with kpi4:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Resilience</div><div class="metric-value">{risk_results["resilience"]}</div></div>', unsafe_allow_html=True)
with kpi5:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Risk Gap</div><div class="metric-value">{risk_results["risk_gap"]}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Main Navigation Tabs
tab_names = [
    "🌎 World Map", "📍 City Analysis", "📊 Risk Analytics", "🌡 Climate",
    "🏥 CHRI Proxy", "🏭 GHG & Carbon", "💧 Water & Effluent", "🌫 Pollution",
    "🌾 Sector Screening", "⚠️ Hazard Screening", "🌐 PostGIS + GeoAI",
    "🛠 Mitigation", "📋 ESG / SDG / ISO", "💾 Export"
]

tabs = st.tabs(tab_names)

# Tab 1: World Map
with tabs[0]:
    st.subheader("Global Geospatial Risk Overview")
    map_fig = build_world_map(cities_df, selected_lat=lat, selected_lon=lon)
    st.plotly_chart(map_fig, use_container_width=True)

# Tab 2: City Analysis
with tabs[1]:
    st.subheader(f"City Spatial Assessment: {selected_city}")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        - **City Name:** {selected_city}
        - **Country:** {selected_country}
        - **Latitude:** `{lat}`
        - **Longitude:** `{lon}`
        - **Estimated Population:** `{pop:,}`
        - **Climate Division:** {climate_division}
        """)
    with c2:
        st.markdown(f"""
        - **Calculated Risk Level:** `{risk_results['risk_category']}`
        - **Action Priority:** `{risk_results['priority']}`
        - **Primary Hazard Driver:** Urban Flood & Extreme Heat
        """)

# Tab 3: Risk Analytics
with tabs[2]:
    st.subheader("Risk Component Distribution")
    chart_df = pd.DataFrame({
        "Component": ["Exposure", "Vulnerability", "Sensitivity", "Criticality", "Adaptive Capacity"],
        "Score": [exposure, vulnerability, sensitivity, criticality, adaptive_capacity]
    })
    fig_bar = px.bar(chart_df, x="Component", y="Score", color="Score", color_continuous_scale="Viridis", height=400)
    fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#E6F1FF")
    st.plotly_chart(fig_bar, use_container_width=True)

# Tab 4: Climate Simulator
with tabs[3]:
    st.subheader(f"Climate Scenario Projections ({climate_scenario} - {scenario_horizon})")
    st.write(f"Projections for **{selected_city}** reflect climate stress level **{risk_results['climate_stress']}**.")

# Tab 5: CHRI Proxy
with tabs[4]:
    st.subheader("AquaGuard CHRI-Style Screening Proxy")
    st.info(f"**Index Assessment:** {risk_results['overall_risk']} / 100. Method: {risk_results['methodology']}")

# Tab 6: GHG & Carbon
with tabs[5]:
    st.subheader("GHG Inventory & Carbon Footprint Engine")
    gc1, gc2, gc3 = st.columns(3)
    fuel = gc1.number_input("Diesel Consumption (Liters)", value=12500.0)
    elec = gc2.number_input("Electricity Usage (kWh)", value=85000.0)
    waste = gc3.number_input("Solid Waste Generated (Tons)", value=120.0)

    ghg_res = calculate_ghg_emissions(fuel, elec, waste)
    carbon_res = get_carbon_footprint_summary(ghg_res, population=pop)

    st.markdown(f"""
    - **Scope 1 (Direct):** `{ghg_res['scope1_tco2e']}` tCO2e
    - **Scope 2 (Electricity):** `{ghg_res['scope2_tco2e']}` tCO2e
    - **Scope 3 (Waste/Indirect):** `{ghg_res['scope3_tco2e']}` tCO2e
    - **Total Carbon Footprint:** `{ghg_res['total_tco2e']}` tCO2e
    """)

# Tab 7: Water & Effluent
with tabs[6]:
    st.subheader("Water Quality & Wastewater Effluent Analysis")
    wc1, wc2 = st.columns(2)
    with wc1:
        ph = st.slider("Water pH", 0.0, 14.0, 7.2)
        tds = st.number_input("TDS (mg/L)", value=450.0)
        do = st.number_input("Dissolved Oxygen (mg/L)", value=6.5)
        w_res = analyze_water_quality(ph, tds, do)
        st.write("Water Quality Risk Score:", w_res["water_quality_risk_score"])
    with wc2:
        bod = st.number_input("Effluent BOD (mg/L)", value=28.0)
        cod = st.number_input("Effluent COD (mg/L)", value=85.0)
        flow = st.number_input("Discharge Flow (m³/day)", value=1500.0)
        e_res = analyze_effluent_discharge(bod, cod, flow)
        st.write("Effluent Risk Score:", e_res["effluent_risk_score"])

# Tab 8: Pollution
with tabs[7]:
    st.subheader("Air Quality Pollution Analysis")
    pc1, pc2, pc3, pc4 = st.columns(4)
    pm25 = pc1.number_input("PM2.5", value=42.0)
    pm10 = pc2.number_input("PM10", value=68.0)
    no2 = pc3.number_input("NO2", value=31.0)
    so2 = pc4.number_input("SO2", value=12.0)
    
    poll_df = analyze_air_pollution(pm25, pm10, no2, so2)
    st.dataframe(poll_df, use_container_width=True)

# Tab 9: Sector Screening
with tabs[8]:
    st.subheader("Global Sector Vulnerability Matrix")
    sector_df = evaluate_sector_risks(risk_results["overall_risk"], hazards_data)
    st.dataframe(sector_df, use_container_width=True)

# Tab 10: Hazard Screening
with tabs[9]:
    st.subheader("Hazard Impact Assessment")
    haz_df = pd.DataFrame([{"Hazard": k, "Score": v["score"], "Category": v["category"]} for k, v in hazards_data.items()])
    st.dataframe(haz_df, use_container_width=True)

# Tab 11: PostGIS + GeoAI
with tabs[10]:
    render_geoai_dashboard(selected_city, selected_country, risk_results)

# Tab 12: Mitigation
with tabs[11]:
    st.subheader("Targeted Mitigation & Climate Adaptation Plan")
    top_h = max(hazards_data, key=lambda k: hazards_data[k]["score"])
    mit_df = generate_mitigation_plan(risk_results["risk_category"], top_h)
    st.dataframe(mit_df, use_container_width=True)
    
    st.markdown("---")
    st.subheader("🤖 AI Executive Interpretation")
    
    ai_context = {
        "city": selected_city,
        "country": selected_country,
        "scenario": climate_scenario,
        "horizon": scenario_horizon,
        "overall_risk": risk_results["overall_risk"],
        "risk_category": risk_results["risk_category"],
        "climate_stress": risk_results["climate_stress"],
        "resilience": risk_results["resilience"],
        "total_co2e": ghg_res["total_tco2e"]
    }
    
    if st.button("Generate AI Assessment Interpretation"):
        with st.spinner("Connecting to AI Interpretation Engine..."):
            ai_text = get_ai_interpretation(ai_context)
            st.markdown(ai_text)

# Tab 13: Sustainability ESG / SDG / ISO
with tabs[12]:
    st.subheader("ESG, SDG, Legacy MDG & ISO Policy Alignment")
    sus_df = get_sustainability_mappings()
    st.dataframe(sus_df, use_container_width=True)

# Tab 14: Export
with tabs[13]:
    st.subheader("Download Assessment Reports & Datasets")
    project_info = {
        "Project": project_name, "Country": selected_country, "City": selected_city,
        "Latitude": lat, "Longitude": lon, "Scenario": climate_scenario, "Horizon": scenario_horizon
    }
    report_bytes = generate_consolidated_report(project_info, risk_results, hazards_data, ghg_res)
    
    st.download_button(
        label="📥 Export Complete Assessment Workbook (.xlsx)",
        data=report_bytes,
        file_name=f"AquaGuard_Assessment_{selected_city}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
