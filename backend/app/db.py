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
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS companies (
                ticker TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                sector TEXT NOT NULL,
                price REAL NOT NULL,
                market_cap_b REAL NOT NULL,
                revenue_growth REAL NOT NULL,
                operating_margin REAL NOT NULL,
                pe_ratio REAL NOT NULL,
                debt_to_equity REAL NOT NULL,
                free_cash_flow_b REAL NOT NULL,
                valuation_score REAL NOT NULL
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
        ("AAPL", "Apple", "Technology", 225.8, 3430, 0.08, 0.31, 34.1, 1.7, 105, 0.0),
        ("MSFT", "Microsoft", "Technology", 426.4, 3170, 0.15, 0.42, 36.8, 0.5, 76, 0.0),
        ("NVDA", "NVIDIA", "Semiconductors", 123.7, 3050, 0.61, 0.57, 62.2, 0.3, 42, 0.0),
        ("AMZN", "Amazon", "Consumer", 179.5, 1880, 0.12, 0.11, 54.4, 0.8, 38, 0.0),
    ]
    with get_conn() as conn:
        conn.executemany(
            "INSERT OR REPLACE INTO investors (cik, name, filing_count, top_holdings) VALUES (?, ?, ?, ?)",
            investors,
        )
        conn.executemany(
            """
            INSERT OR REPLACE INTO companies
            (ticker, name, sector, price, market_cap_b, revenue_growth, operating_margin, pe_ratio, debt_to_equity, free_cash_flow_b, valuation_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            companies,
        )
