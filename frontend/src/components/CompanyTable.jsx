import { Link } from 'react-router-dom'
import Sparkline from './Sparkline'

export default function CompanyTable({ companies }) {
  return (
    <table>
      <thead>
        <tr>
          <th>티커명</th>
          <th>기업명</th>
          <th>주요 섹터</th>
          <th>현재 가격</th>
          <th>최근 가격 추이</th>
          <th>그레이엄 지수</th>
          <th>PEG 기반 적정가</th>
          <th>종합 평가지수</th>
        </tr>
      </thead>
      <tbody>
        {companies.map((company) => (
          <tr key={company.ticker}>
            <td><Link to={`/company/${company.ticker}`}>{company.ticker}</Link></td>
            <td>{company.name}</td>
            <td>{company.sector_ko}</td>
            <td>${company.price.toFixed(2)}</td>
            <td><Sparkline values={company.price_trend} /></td>
            <td>{company.graham_index}</td>
            <td>{company.peg_fair_price}</td>
            <td>{company.composite_score}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
