from __future__ import annotations

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "portfolio.db"


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS investors (
                cik TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                filing_count INTEGER NOT NULL,
                top_holdings TEXT NOT NULL
            )
            """
        )
        conn.execute("DROP TABLE IF EXISTS companies")
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS companies (
                ticker TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                sector_ko TEXT NOT NULL,
                price REAL NOT NULL,
                price_trend TEXT NOT NULL,
                eps REAL NOT NULL,
                bps REAL NOT NULL,
                eps_growth_rate REAL NOT NULL,
                roe REAL NOT NULL,
                per REAL NOT NULL,
                revenue_growth_pct REAL NOT NULL,
                graham_index REAL NOT NULL,
                peg_fair_price REAL NOT NULL,
                composite_score REAL NOT NULL
            )
            """
        )


def seed_data() -> None:
    investors = [
        ("0001067983", "Berkshire Hathaway", 287, "AAPL, BAC, AXP"),
        ("0001037389", "Bridgewater Associates", 145, "SPY, IVV, VWO"),
        ("0001167483", "Scion Asset Management", 46, "GOOG, JD, HCA"),
    ]
    companies = [
        ("AAPL", "Apple", "기술", 225.8, "201,208,212,220,223,225", 6.43, 4.85, 11.2, 172.5, 34.1, 8.0, 0.0, 0.0, 0.0),
        ("MSFT", "Microsoft", "기술", 426.4, "391,396,404,411,419,426", 11.56, 36.1, 14.5, 38.2, 36.8, 15.0, 0.0, 0.0, 0.0),
        ("NVDA", "NVIDIA", "반도체", 123.7, "97,102,109,113,118,123", 1.30, 2.15, 45.0, 74.0, 62.2, 61.0, 0.0, 0.0, 0.0),
        ("AMZN", "Amazon", "소비재", 179.5, "153,160,166,171,176,179", 4.02, 20.5, 23.5, 24.0, 54.4, 12.0, 0.0, 0.0, 0.0),
    ]
    with get_conn() as conn:
        conn.executemany(
            "INSERT OR REPLACE INTO investors (cik, name, filing_count, top_holdings) VALUES (?, ?, ?, ?)",
            investors,
        )
        conn.executemany(
            """
            INSERT OR REPLACE INTO companies
            (ticker, name, sector_ko, price, price_trend, eps, bps, eps_growth_rate, roe, per, revenue_growth_pct, graham_index, peg_fair_price, composite_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            companies,
        )
