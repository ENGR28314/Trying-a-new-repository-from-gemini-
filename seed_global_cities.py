
import sys
import os
from sqlalchemy import text
from db import get_db_engine

FALLBACK_CITIES = [
    {"name": "New York", "country": "United States", "country_code": "USA", "lat": 40.7128, "lon": -74.0060, "pop": 8335897},
    {"name": "London", "country": "United Kingdom", "country_code": "GBR", "lat": 51.5074, "lon": -0.1278, "pop": 8982000},
    {"name": "Tokyo", "country": "Japan", "country_code": "JPN", "lat": 35.6762, "lon": 139.6503, "pop": 13960000},
    {"name": "Karachi", "country": "Pakistan", "country_code": "PAK", "lat": 24.8607, "lon": 67.0011, "pop": 14910000},
    {"name": "Lahore", "country": "Pakistan", "country_code": "PAK", "lat": 31.5204, "lon": 74.3587, "pop": 11130000},
    {"name": "Islamabad", "country": "Pakistan", "country_code": "PAK", "lat": 33.6844, "lon": 73.0479, "pop": 1015000},
    {"name": "Cairo", "country": "Egypt", "country_code": "EGY", "lat": 30.0444, "lon": 31.2357, "pop": 9500000},
    {"name": "São Paulo", "country": "Brazil", "country_code": "BRA", "lat": -23.5505, "lon": -46.6333, "pop": 12330000},
    {"name": "Sydney", "country": "Australia", "country_code": "AUS", "lat": -33.8688, "lon": 151.2093, "pop": 5312000},
    {"name": "Mumbai", "country": "India", "country_code": "IND", "lat": 19.0760, "lon": 72.8777, "pop": 12442000},
]

def seed_cities():
    engine, connected = get_db_engine()
    if not connected:
        print("[ERROR] Cannot seed database. PostgreSQL connection failed.")
        return

    with engine.begin() as conn:
        for c in FALLBACK_CITIES:
            query = text("""
                INSERT INTO cities (name, country, country_code, latitude, longitude, population, geometry)
                VALUES (:name, :country, :country_code, :lat, :lon, :pop, ST_SetSRID(ST_MakePoint(:lon, :lat), 4326))
                ON CONFLICT DO NOTHING;
            """)
            conn.execute(query, c)
    print(f"[SUCCESS] Successfully seeded {len(FALLBACK_CITIES)} default cities into PostGIS database.")

if __name__ == "__main__":
    seed_cities()
