const BASE_URL = 'http://localhost:8000/api'

export async function getCompanies() {
  const res = await fetch(`${BASE_URL}/companies`)
  return res.json()
}

export async function getInvestors() {
  const res = await fetch(`${BASE_URL}/investors`)
  return res.json()
}

export async function getCompany(ticker) {
  const res = await fetch(`${BASE_URL}/companies/${ticker}`)
  return res.json()
}

export async function getReport(ticker) {
  const res = await fetch(`${BASE_URL}/companies/${ticker}/report`)
  return res.json()
}
