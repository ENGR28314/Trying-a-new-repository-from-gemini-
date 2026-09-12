
import pandas as pd
import plotly.express as px
from sqlalchemy import text
from db import get_cached_engine

FALLBACK_MAP_DATA = pd.DataFrame([
    {"name": "New York", "country": "United States", "latitude": 40.7128, "longitude": -74.0060, "population": 8335897, "risk_score": 45.0, "risk_level": "Moderate"},
    {"name": "London", "country": "United Kingdom", "latitude": 51.5074, "longitude": -0.1278, "population": 8982000, "risk_score": 32.0, "risk_level": "Low"},
    {"name": "Tokyo", "country": "Japan", "latitude": 35.6762, "longitude": 139.6503, "population": 13960000, "risk_score": 62.0, "risk_level": "Moderate"},
    {"name": "Karachi", "country": "Pakistan", "latitude": 24.8607, "longitude": 67.0011, "population": 14910000, "risk_score": 78.0, "risk_level": "High"},
    {"name": "Lahore", "country": "Pakistan", "latitude": 31.5204, "longitude": 74.3587, "population": 11130000, "risk_score": 82.0, "risk_level": "High"},
    {"name": "Cairo", "country": "Egypt", "latitude": 30.0444, "longitude": 31.2357, "population": 9500000, "risk_score": 71.0, "risk_level": "High"}
])

def load_cities_from_db():
    engine, connected = get_cached_engine()
    if not connected:
        return FALLBACK_MAP_DATA, False

    try:
        query = text("SELECT id, name, country, country_code, latitude, longitude, population FROM cities;")
        with engine.connect() as conn:
            df = pd.read_sql(query, conn)
            if df.empty:
                return FALLBACK_MAP_DATA, False
            
            df["risk_score"] = 55.0  # Dynamic baseline indicator
            df["risk_level"] = "Moderate"
            return df, True
    except Exception:
        return FALLBACK_MAP_DATA, False

def build_world_map(df_cities: pd.DataFrame, selected_lat: float = None, selected_lon: float = None):
    fig = px.scatter_mapbox(
        df_cities,
        lat="latitude",
        lon="longitude",
        hover_name="name",
        hover_data=["country", "population", "risk_score"],
        color_discrete_sequence=["#00E5FF"],
        size_max=15,
        zoom=1.5,
        height=550
    )
    
    if selected_lat and selected_lon:
        fig.add_trace(
            px.scatter_mapbox(
                pd.DataFrame([{"lat": selected_lat, "lon": selected_lon, "name": "Selected Site"}]),
                lat="lat",
                lon="lon",
                hover_name="name"
            ).data[0]
        )
        # Style focal point marker bright cyan red target
        fig.data[-1].marker.color = "#FF2A6D"
        fig.data[-1].marker.size = 18

    fig.update_layout(
        mapbox_style="carto-darkmatter",
        margin={"r":0,"t":0,"l":0,"b":0},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig
