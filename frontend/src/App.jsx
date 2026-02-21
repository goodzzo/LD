import { Route, Routes, useParams } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { getCompanies, getCompany, getInvestors, getReport } from './api/client'
import CompanyTable from './components/CompanyTable'

function Dashboard() {
  const [companies, setCompanies] = useState([])
  const [investors, setInvestors] = useState([])

  useEffect(() => {
    getCompanies().then(setCompanies)
    getInvestors().then(setInvestors)
  }, [])

  return (
    <div className="container">
      <h1>투자 인텔리전스 대시보드</h1>
      <section>
        <h2>Nasdaq 주요 기업 가치평가</h2>
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
      <p>섹터: {company.sector}</p>
      <p>PER: {company.pe_ratio}</p>
      <p>Debt/Equity: {company.debt_to_equity}</p>
      <p>FCF(십억$): {company.free_cash_flow_b}</p>
      <p>Valuation Score: {company.valuation_score}</p>

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
