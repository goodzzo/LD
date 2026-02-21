# Investor Intelligence Lab (LD)

Git, Ollama, 프론트엔드/백엔드 에이전트, 오케스트레이션을 한 번에 학습할 수 있는 **통합 학습 프로젝트**입니다.

## 목표
- 13F 공시 기반 기관/투자 대가 포트폴리오 수집
- Nasdaq 주요 기업의 재무/시장 데이터 수집
- 계산식 기반 종합 가치평가 점수 산출
- 기업 상세 페이지에서 Local LLM(Ollama) 기반 리포트 생성

## 아키텍처

```text
[Scheduler/Orchestrator]
   ├── 13F Ingestion Agent  ---> [PostgreSQL]
   ├── Market Data Agent    ---> [PostgreSQL]
   └── Valuation Agent      ---> [PostgreSQL: score cache]

[FastAPI Backend]
   ├── /institutions
   ├── /companies
   ├── /companies/{ticker}/valuation
   └── /companies/{ticker}/report  ---> [Ollama]

[React Frontend]
   ├── Dashboard (기관 + 기업 요약)
   ├── Company List (필터/정렬)
   └── Company Detail (valuation + LLM report)
```

## 실행 순서 (학습용)
1. DB 실행: `docker compose up -d db`
2. 백엔드 실행: `uvicorn app.main:app --reload --app-dir backend`
3. 프론트 실행: `npm install && npm run dev` (frontend)
4. 오케스트레이터 실행: `python orchestrator/run_pipeline.py`

## 디렉터리
- `backend/`: FastAPI + SQLModel 기반 API
- `frontend/`: React 대시보드
- `orchestrator/`: 수집/계산 파이프라인 실행
- `scripts/`: 초기 스키마/시드 파일

## 다음 확장 아이디어
- Redis 캐시 + 백그라운드 작업 큐(Celery/RQ)
- 13F 원문 파싱 자동화(SEC EDGAR)
- 멀티 에이전트 협업(분석 에이전트, 검증 에이전트, 리포트 에이전트)
