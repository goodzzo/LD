CREATE TABLE IF NOT EXISTS institutions (
  id SERIAL PRIMARY KEY,
  cik VARCHAR(20) UNIQUE NOT NULL,
  name TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS holdings (
  id SERIAL PRIMARY KEY,
  institution_id INT NOT NULL REFERENCES institutions(id) ON DELETE CASCADE,
  ticker VARCHAR(12) NOT NULL,
  shares NUMERIC NOT NULL,
  filing_date DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS companies (
  ticker VARCHAR(12) PRIMARY KEY,
  name TEXT NOT NULL,
  sector TEXT,
  market_cap NUMERIC,
  revenue_growth_yoy NUMERIC,
  operating_margin NUMERIC,
  debt_to_equity NUMERIC,
  valuation_score NUMERIC,
  updated_at TIMESTAMP DEFAULT NOW()
);
