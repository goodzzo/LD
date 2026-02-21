from __future__ import annotations

import httpx


def generate_company_report(ticker: str, company: dict) -> str:
    prompt = (
        f"You are a financial analyst. Write a concise Korean report for {ticker}. "
        f"Use the data: {company}. Include growth drivers, risks, and watch points."
    )

    payload = {
        "model": "llama3.1",
        "prompt": prompt,
        "stream": False,
    }

    try:
        response = httpx.post("http://localhost:11434/api/generate", json=payload, timeout=12)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "LLM 응답이 비어 있습니다.")
    except Exception:
        return (
            f"[{ticker}] 로컬 LLM 연결에 실패하여 템플릿 리포트를 반환합니다. "
            f"매출 성장률 {company['revenue_growth']:.0%}, 영업이익률 {company['operating_margin']:.0%}, "
            f"밸류에이션 점수 {company['valuation_score']}점을 기록했습니다. "
            "핵심 리스크는 고평가 및 매크로 민감도이며, 분기 실적과 현금흐름 추이를 모니터링하세요."
        )
