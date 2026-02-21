from pydantic import BaseModel


class Investor(BaseModel):
    cik: str
    name: str
    filing_count: int
    top_holdings: list[str]


class Company(BaseModel):
    ticker: str
    name: str
    sector_ko: str
    price: float
    price_trend: list[float]
    graham_index: float
    peg_fair_price: float
    composite_score: float


class CompanyDetail(Company):
    eps: float
    bps: float
    eps_growth_rate: float
    roe: float
    per: float
    revenue_growth_pct: float


class LlmReport(BaseModel):
    ticker: str
    model: str
    report: str


class OrchestrationStatus(BaseModel):
    run_id: str
    steps: list[str]
    summary: str


class ApiQuota(BaseModel):
    provider: str
    used: int
    limit: int
    status: str
