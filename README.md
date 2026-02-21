# Investor Intelligence Playground

Git + Ollama + 프론트엔드/백엔드 에이전트 + 오케스트레이션 개념을 한 번에 연습할 수 있는 학습용 프로젝트입니다.

## 목표
- 13F 기관/투자 대가 데이터를 백엔드 SQLite DB에 저장
- Nasdaq 주요 기업 데이터를 관리하고 계산식 기반 기업 가치평가 점수 산출
- React 대시보드에서 리스트/상세 페이지 제공
- 상세 페이지에서 Local LLM(Ollama) 기반 기업 리포트 생성
- `GitAgent -> BackendAgent -> FrontendAgent` 오케스트레이션 체험

## 핵심 지표 수식
- 그레이엄 지수: `sqrt(22.5 * EPS * BPS)`
- PEG 기반 적정가: `EPS * EPS Growth Rate * 1`
- 최종 평가 종합 점수: `(ROE / PER) * Revenue Growth(%)`

## 아키텍처
- `backend/app/main.py`: FastAPI API 진입점
- `backend/app/db.py`: SQLite 스키마/시드
- `backend/app/services.py`: 가치평가 계산 로직
- `backend/app/providers.py`: Nasdaq 공급자/쿼터 상태
- `backend/app/llm.py` + `backend/app/prompts/company_report_prompt.txt`: Ollama 프롬프트 관리
- `backend/app/agents.py`: 에이전트 오케스트레이션
- `frontend/src/App.jsx`: 대시보드 + 상세 페이지

## 빠른 시작
### 1) 백엔드
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 2) 프론트엔드
```bash
cd frontend
npm install
npm run dev
```

### 3) Ollama (선택)
```bash
ollama serve
ollama pull llama3.1
```

Ollama 미실행 시에도 템플릿 리포트로 fallback 됩니다.

## API 예시
- `GET /api/investors`
- `GET /api/companies`
- `GET /api/companies/{ticker}`
- `GET /api/companies/{ticker}/report`
- `GET /api/system/quota`
- `POST /api/orchestrate/refresh`
