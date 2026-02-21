from pydantic import BaseModel


class Investor(BaseModel):
    cik: str
    name: str
    filing_count: int
    top_holdings: list[str]


class Company(BaseModel):
    ticker: str
    name: str
    sector: str
    price: float
    market_cap_b: float
    revenue_growth: float
    operating_margin: float
    valuation_score: float


class CompanyDetail(Company):
    pe_ratio: float
    debt_to_equity: float
    free_cash_flow_b: float


class LlmReport(BaseModel):
    ticker: str
    model: str
    report: str


class OrchestrationStatus(BaseModel):
    run_id: str
    steps: list[str]
    summary: str
