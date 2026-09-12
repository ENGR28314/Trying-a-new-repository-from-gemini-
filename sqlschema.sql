
-- Enable PostGIS spatial extension
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Projects Table
CREATE TABLE IF NOT EXISTS projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    country VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    climate_division VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Countries Table
CREATE TABLE IF NOT EXISTS countries (
    iso_code VARCHAR(3) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    region VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Cities Table (PostGIS Spatial)
CREATE TABLE IF NOT EXISTS cities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    country VARCHAR(100) NOT NULL,
    country_code VARCHAR(3) NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    population BIGINT DEFAULT 0,
    geometry GEOMETRY(Point, 4326),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_cities_geometry ON cities USING GIST (geometry);
CREATE INDEX IF NOT EXISTS idx_cities_country_code ON cities (country_code);

-- 4. Environmental Observations Table
CREATE TABLE IF NOT EXISTS environmental_observations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    city_id INT REFERENCES cities(id) ON DELETE CASCADE,
    variable_name VARCHAR(100) NOT NULL,
    observed_value DOUBLE PRECISION NOT NULL,
    unit VARCHAR(30) NOT NULL,
    threshold_value DOUBLE PRECISION,
    source VARCHAR(255) DEFAULT 'User Upload',
    observation_year INT DEFAULT 2026,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 5. Risk Assessments Table
CREATE TABLE IF NOT EXISTS risk_assessments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_name VARCHAR(255) NOT NULL,
    country VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    climate_scenario VARCHAR(50) NOT NULL,
    scenario_horizon VARCHAR(50) NOT NULL,
    overall_risk DOUBLE PRECISION NOT NULL,
    risk_category VARCHAR(50) NOT NULL,
    exposure DOUBLE PRECISION NOT NULL,
    vulnerability DOUBLE PRECISION NOT NULL,
    sensitivity DOUBLE PRECISION NOT NULL,
    adaptive_capacity DOUBLE PRECISION NOT NULL,
    criticality DOUBLE PRECISION NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 6. Hazard Assessments Table
CREATE TABLE IF NOT EXISTS hazard_assessments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    assessment_id UUID REFERENCES risk_assessments(id) ON DELETE CASCADE,
    hazard_type VARCHAR(100) NOT NULL,
    hazard_score DOUBLE PRECISION NOT NULL,
    risk_level VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 7. Sector Assessments Table
CREATE TABLE IF NOT EXISTS sector_assessments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    assessment_id UUID REFERENCES risk_assessments(id) ON DELETE CASCADE,
    sector_name VARCHAR(100) NOT NULL,
    sector_score DOUBLE PRECISION NOT NULL,
    risk_level VARCHAR(50) NOT NULL,
    top_hazard VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 8. GHG Assessments Table
CREATE TABLE IF NOT EXISTS ghg_assessments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    assessment_id UUID REFERENCES risk_assessments(id) ON DELETE CASCADE,
    scope1_co2e DOUBLE PRECISION DEFAULT 0.0,
    scope2_co2e DOUBLE PRECISION DEFAULT 0.0,
    scope3_co2e DOUBLE PRECISION DEFAULT 0.0,
    total_co2e DOUBLE PRECISION DEFAULT 0.0,
    unit VARCHAR(20) DEFAULT 'tCO2e',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 9. Mitigation Actions Table
CREATE TABLE IF NOT EXISTS mitigation_actions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    assessment_id UUID REFERENCES risk_assessments(id) ON DELETE CASCADE,
    risk_driver VARCHAR(100) NOT NULL,
    sector VARCHAR(100) NOT NULL,
    mitigation_measure TEXT NOT NULL,
    adaptation_measure TEXT NOT NULL,
    priority VARCHAR(20) NOT NULL,
    esg_area VARCHAR(50),
    sdg_target VARCHAR(100),
    iso_framework VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
