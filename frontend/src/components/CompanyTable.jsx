import { Link } from 'react-router-dom'

export default function CompanyTable({ companies }) {
  return (
    <table>
      <thead>
        <tr>
          <th>티커</th>
          <th>기업명</th>
          <th>섹터</th>
          <th>가격</th>
          <th>점수</th>
        </tr>
      </thead>
      <tbody>
        {companies.map((company) => (
          <tr key={company.ticker}>
            <td>
              <Link to={`/company/${company.ticker}`}>{company.ticker}</Link>
            </td>
            <td>{company.name}</td>
            <td>{company.sector}</td>
            <td>${company.price}</td>
            <td>{company.valuation_score}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
