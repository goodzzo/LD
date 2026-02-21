from __future__ import annotations

import math

from .db import get_conn


def calculate_graham_index(eps: float, bps: float) -> float:
    return round(math.sqrt(22.5 * eps * bps), 2)


def calculate_peg_fair_price(eps: float, eps_growth_rate: float) -> float:
    return round(eps * eps_growth_rate * 1, 2)


def calculate_composite_score(roe: float, per: float, revenue_growth_pct: float) -> float:
    if per <= 0:
        return 0.0
    return round((roe / per) * revenue_growth_pct, 2)


def refresh_company_scores() -> None:
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM companies").fetchall()
        for row in rows:
            graham_index = calculate_graham_index(row["eps"], row["bps"])
            peg_fair_price = calculate_peg_fair_price(row["eps"], row["eps_growth_rate"])
            composite_score = calculate_composite_score(row["roe"], row["per"], row["revenue_growth_pct"])
            conn.execute(
                "UPDATE companies SET graham_index = ?, peg_fair_price = ?, composite_score = ? WHERE ticker = ?",
                (graham_index, peg_fair_price, composite_score, row["ticker"]),
            )


def _row_to_company_payload(row: dict) -> dict:
    payload = dict(row)
    payload["price_trend"] = [float(v) for v in payload["price_trend"].split(",")]
    return payload


def list_companies() -> list[dict]:
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM companies ORDER BY composite_score DESC").fetchall()
    return [_row_to_company_payload(row) for row in rows]


def get_company(ticker: str) -> dict | None:
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM companies WHERE ticker = ?", (ticker.upper(),)).fetchone()
    return _row_to_company_payload(row) if row else None


def list_investors() -> list[dict]:
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM investors ORDER BY filing_count DESC").fetchall()

    result: list[dict] = []
    for row in rows:
        item = dict(row)
        item["top_holdings"] = [h.strip() for h in item["top_holdings"].split(",")]
        result.append(item)
    return result
