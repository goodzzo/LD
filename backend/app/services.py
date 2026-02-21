from __future__ import annotations

from dataclasses import asdict, dataclass

from .db import get_conn


@dataclass
class CompanyRow:
    ticker: str
    name: str
    sector: str
    price: float
    market_cap_b: float
    revenue_growth: float
    operating_margin: float
    pe_ratio: float
    debt_to_equity: float
    free_cash_flow_b: float
    valuation_score: float


def calculate_valuation_score(
    revenue_growth: float,
    operating_margin: float,
    pe_ratio: float,
    debt_to_equity: float,
    free_cash_flow_b: float,
) -> float:
    growth_score = min(max(revenue_growth * 120, 0), 40)
    margin_score = min(max(operating_margin * 80, 0), 25)
    pe_score = min(max((60 - pe_ratio) * 0.5, 0), 20)
    debt_score = min(max((2.5 - debt_to_equity) * 6, 0), 10)
    cash_flow_score = min(max(free_cash_flow_b / 8, 0), 5)
    return round(growth_score + margin_score + pe_score + debt_score + cash_flow_score, 2)


def refresh_company_scores() -> None:
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM companies").fetchall()
        for row in rows:
            score = calculate_valuation_score(
                revenue_growth=row["revenue_growth"],
                operating_margin=row["operating_margin"],
                pe_ratio=row["pe_ratio"],
                debt_to_equity=row["debt_to_equity"],
                free_cash_flow_b=row["free_cash_flow_b"],
            )
            conn.execute(
                "UPDATE companies SET valuation_score = ? WHERE ticker = ?",
                (score, row["ticker"]),
            )


def list_companies() -> list[dict]:
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM companies ORDER BY valuation_score DESC").fetchall()
        return [dict(row) for row in rows]


def get_company(ticker: str) -> dict | None:
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM companies WHERE ticker = ?", (ticker.upper(),)).fetchone()
        return dict(row) if row else None


def list_investors() -> list[dict]:
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM investors ORDER BY filing_count DESC").fetchall()

    result: list[dict] = []
    for row in rows:
        item = dict(row)
        item["top_holdings"] = [h.strip() for h in item["top_holdings"].split(",")]
        result.append(item)
    return result
