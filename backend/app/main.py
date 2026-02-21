from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .agents import Orchestrator
from .db import init_db, seed_data
from .llm import generate_company_report
from .providers import NasdaqProvider
from .schemas import ApiQuota, Company, CompanyDetail, Investor, LlmReport, OrchestrationStatus
from .services import get_company, list_companies, list_investors, refresh_company_scores

app = FastAPI(title="Investor Intelligence Platform")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    init_db()
    seed_data()
    refresh_company_scores()


@app.get("/api/investors", response_model=list[Investor])
def investors() -> list[Investor]:
    return [Investor(**row) for row in list_investors()]


@app.get("/api/companies", response_model=list[Company])
def companies() -> list[Company]:
    return [Company(**row) for row in list_companies()]


@app.get("/api/companies/{ticker}", response_model=CompanyDetail)
def company_detail(ticker: str) -> CompanyDetail:
    company = get_company(ticker)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return CompanyDetail(**company)


@app.get("/api/companies/{ticker}/report", response_model=LlmReport)
def company_report(ticker: str) -> LlmReport:
    company = get_company(ticker)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    report = generate_company_report(ticker.upper(), company)
    return LlmReport(ticker=ticker.upper(), model="llama3.1", report=report)


@app.get("/api/system/quota", response_model=ApiQuota)
def api_quota() -> ApiQuota:
    provider = NasdaqProvider()
    return ApiQuota(**provider.quota())


@app.post("/api/orchestrate/refresh", response_model=OrchestrationStatus)
def orchestrate_refresh() -> OrchestrationStatus:
    orchestrator = Orchestrator()
    return OrchestrationStatus(**orchestrator.run())
