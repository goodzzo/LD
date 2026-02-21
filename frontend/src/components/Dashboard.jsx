import { useEffect, useState } from "react";

export function Dashboard() {
  const [companies, setCompanies] = useState([]);
  const [selected, setSelected] = useState(null);
  const [report, setReport] = useState("Click a ticker to generate local LLM report.");

  useEffect(() => {
    fetch("http://localhost:8000/companies")
      .then((r) => r.json())
      .then(setCompanies)
      .catch(() => setCompanies([]));
  }, []);

  const loadReport = async (ticker) => {
    setSelected(ticker);
    setReport("Generating report via Ollama...");
    try {
      const res = await fetch(`http://localhost:8000/companies/${ticker}/report`);
      const body = await res.json();
      setReport(body.report || "No report returned.");
    } catch {
      setReport("Failed to load report. Check backend/Ollama.");
    }
  };

  return (
    <main style={{ fontFamily: "sans-serif", margin: "24px" }}>
      <h1>Investor Intelligence Lab</h1>
      <p>13F + Nasdaq + Local LLM 기반 기업 분석 대시보드</p>

      <section>
        <h2>Company List</h2>
        <ul>
          {companies.map((c) => (
            <li key={c.ticker}>
              <button onClick={() => loadReport(c.ticker)}>{c.ticker}</button>
              {" "}- {c.name} / Score: {c.valuation_score}
            </li>
          ))}
        </ul>
      </section>

      <section>
        <h2>LLM Report {selected ? `(${selected})` : ""}</h2>
        <pre style={{ whiteSpace: "pre-wrap", background: "#f6f8fa", padding: "12px" }}>{report}</pre>
      </section>
    </main>
  );
}
