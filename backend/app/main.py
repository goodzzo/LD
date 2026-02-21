from typing import Optional

import httpx
from fastapi import FastAPI, HTTPException
from sqlmodel import Field, SQLModel

app = FastAPI(title="Investor Intelligence Lab API")


class CompanyBase(SQLModel):
    ticker: str = Field(index=True)
    name: str
    sector: str
    market_cap: float
    revenue_growth_yoy: float
    operating_margin: float
    debt_to_equity: float


class CompanyResponse(CompanyBase):
    valuation_score: float


def calculate_valuation_score(
    revenue_growth_yoy: float,
    operating_margin: float,
    debt_to_equity: float,
    market_cap: float,
) -> float:
    growth_factor = max(min(revenue_growth_yoy * 1.5, 40), -20)
    profitability_factor = max(min(operating_margin * 1.2, 35), -20)
    leverage_penalty = max(min(debt_to_equity * 8, 30), 0)
    scale_bonus = 10 if market_cap > 200_000_000_000 else 4
    raw = 50 + growth_factor + profitability_factor - leverage_penalty + scale_bonus
    return round(max(min(raw, 100), 0), 2)


SAMPLE_COMPANIES = [
    {
        "ticker": "AAPL",
        "name": "Apple Inc.",
        "sector": "Technology",
        "market_cap": 2_900_000_000_000,
        "revenue_growth_yoy": 8.2,
        "operating_margin": 29.8,
        "debt_to_equity": 1.7,
    },
    {
        "ticker": "MSFT",
        "name": "Microsoft Corporation",
        "sector": "Technology",
        "market_cap": 3_100_000_000_000,
        "revenue_growth_yoy": 16.3,
        "operating_margin": 42.1,
        "debt_to_equity": 0.6,
    },
]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/companies", response_model=list[CompanyResponse])
def list_companies(sector: Optional[str] = None) -> list[CompanyResponse]:
    rows = SAMPLE_COMPANIES
    if sector:
        rows = [item for item in rows if item["sector"].lower() == sector.lower()]

    response: list[CompanyResponse] = []
    for item in rows:
        score = calculate_valuation_score(
            item["revenue_growth_yoy"],
            item["operating_margin"],
            item["debt_to_equity"],
            item["market_cap"],
        )
        response.append(CompanyResponse(**item, valuation_score=score))
    return response


@app.get("/companies/{ticker}/report")
async def company_report(ticker: str) -> dict[str, str]:
    company = next((item for item in SAMPLE_COMPANIES if item["ticker"] == ticker.upper()), None)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    prompt = (
        f"Generate a concise investment report for {company['name']} ({company['ticker']}). "
        f"Include growth, margin, leverage, and risk factors."
    )

    async with httpx.AsyncClient(timeout=90) as client:
        try:
            res = await client.post(
                "http://localhost:11434/api/generate",
                json={"model": "llama3.1", "prompt": prompt, "stream": False},
            )
            res.raise_for_status()
        except httpx.HTTPError as exc:
            raise HTTPException(status_code=502, detail=f"Ollama call failed: {exc}") from exc

    return {"ticker": ticker.upper(), "report": res.json().get("response", "")}
