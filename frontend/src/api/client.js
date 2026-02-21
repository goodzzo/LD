const BASE_URL = 'http://localhost:8000/api'

async function asJson(path) {
  const res = await fetch(`${BASE_URL}${path}`)
  if (!res.ok) throw new Error(`API error: ${path}`)
  return res.json()
}

export function getCompanies() {
  return asJson('/companies')
}

export function getInvestors() {
  return asJson('/investors')
}

export function getCompany(ticker) {
  return asJson(`/companies/${ticker}`)
}

export function getReport(ticker) {
  return asJson(`/companies/${ticker}/report`)
}

export function getApiQuota() {
  return asJson('/system/quota')
}
