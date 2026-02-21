from __future__ import annotations

from pathlib import Path

import httpx

PROMPT_FILE = Path(__file__).resolve().parent / "prompts" / "company_report_prompt.txt"


def _build_prompt(ticker: str, company: dict) -> str:
    template = PROMPT_FILE.read_text(encoding="utf-8")
    return template.format(ticker=ticker, **company)


def generate_company_report(ticker: str, company: dict) -> str:
    payload = {
        "model": "llama3.1",
        "prompt": _build_prompt(ticker, company),
        "stream": False,
        "options": {
            "temperature": 0.4, # 분석의 일관성을 위해 온도를 낮게 설정
            "top_p": 0.9
        }
    }

    try:
        response = httpx.post("http://localhost:11434/api/generate", json=payload, timeout=20)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "LLM 응답이 비어 있습니다.")
    except Exception:
        return (
            f"[{ticker}] 로컬 LLM 연결에 실패하여 템플릿 리포트를 반환합니다. "
            f"그레이엄 지수 {company['graham_index']}, PEG 기반 적정가 {company['peg_fair_price']}, "
            f"종합 평가지수 {company['composite_score']}를 기록했습니다. "
            "주요 리스크는 밸류에이션 변동성과 거시경제 민감도입니다."
        )
