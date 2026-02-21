import { Route, Routes, useParams } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { getApiQuota, getCompanies, getCompany, getInvestors, getReport } from './api/client'
import CompanyTable from './components/CompanyTable'
import QuotaBadge from './components/QuotaBadge'

function Dashboard() {
  const [companies, setCompanies] = useState([])
  const [investors, setInvestors] = useState([])
  const [quota, setQuota] = useState(null)

  useEffect(() => {
    getCompanies().then(setCompanies)
    getInvestors().then(setInvestors)
    getApiQuota().then(setQuota)
  }, [])

  return (
    <div className="container">
      <h1>투자 인텔리전스 대시보드</h1>
      <p className="subtitle">현대적이고 클래식한 UI로 핵심 밸류에이션 지표를 빠르게 확인하세요.</p>

      <section>
        <h2>Nasdaq 주요 기업 종합 평가</h2>
        <CompanyTable companies={companies} />
      </section>

      <section>
        <h2>투자 대가/13F 기관</h2>
        <ul>
          {investors.map((investor) => (
            <li key={investor.cik}>
              {investor.name} ({investor.filing_count} filings) - {investor.top_holdings.join(', ')}
            </li>
          ))}
        </ul>
      </section>

      <QuotaBadge quota={quota} />
    </div>
  )
}

function CompanyDetailPage() {
  const { ticker } = useParams()
  const [company, setCompany] = useState(null)
  const [report, setReport] = useState('')

  useEffect(() => {
    getCompany(ticker).then(setCompany)
    getReport(ticker).then((res) => setReport(res.report))
  }, [ticker])

  if (!company) return <p>로딩 중...</p>

  return (
    <div className="container">
      <h1>{company.name} ({company.ticker})</h1>
      <p>주요 섹터: {company.sector_ko}</p>
      <p>EPS: {company.eps}</p>
      <p>BPS: {company.bps}</p>
      <p>ROE: {company.roe}</p>
      <p>PER: {company.per}</p>
      <p>Revenue Growth(%): {company.revenue_growth_pct}</p>
      <p>Graham Index: {company.graham_index}</p>
      <p>PEG Fair Price: {company.peg_fair_price}</p>
      <p>Composite Score: {company.composite_score}</p>

      <h2>Local LLM Report</h2>
      <pre>{report}</pre>
    </div>
  )
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Dashboard />} />
      <Route path="/company/:ticker" element={<CompanyDetailPage />} />
    </Routes>
  )
}
