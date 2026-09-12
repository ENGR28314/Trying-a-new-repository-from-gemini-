
import os
import streamlit as st
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

def get_db_credentials():
    """Extracts PostgreSQL credentials from Streamlit Secrets or environment variables."""
    try:
        if "postgresql" in st.secrets:
            pg = st.secrets["postgresql"]
            return pg["host"], pg["port"], pg["database"], pg["username"], pg["password"]
    except Exception:
        pass
    
    return (
        os.getenv("POSTGRES_HOST", "localhost"),
        os.getenv("POSTGRES_PORT", "5432"),
        os.getenv("POSTGRES_DB", "aquaguard"),
        os.getenv("POSTGRES_USER", "postgres"),
        os.getenv("POSTGRES_PASSWORD", "postgres")
    )

def get_db_engine():
    """Creates a SQLAlchemy engine for PostgreSQL / PostGIS."""
    host, port, db, user, pwd = get_db_credentials()
    db_url = f"postgresql://{user}:{pwd}@{host}:{port}/{db}"
    try:
        engine = create_engine(db_url, pool_pre_ping=True, connect_args={"connect_timeout": 3})
        # Quick validation ping
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return engine, True
    except Exception as e:
        return None, False

@st.cache_resource
def get_cached_engine():
    return get_db_engine()
