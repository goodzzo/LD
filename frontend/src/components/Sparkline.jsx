export default function Sparkline({ values = [] }) {
  if (!values.length) return null
  const min = Math.min(...values)
  const max = Math.max(...values)
  const range = max - min || 1
  const points = values
    .map((v, i) => `${(i / (values.length - 1)) * 100},${40 - ((v - min) / range) * 36}`)
    .join(' ')

  return (
    <svg width="120" height="40" viewBox="0 0 100 40" className="sparkline">
      <polyline fill="none" stroke="#2f5fd0" strokeWidth="2" points={points} />
    </svg>
  )
}
