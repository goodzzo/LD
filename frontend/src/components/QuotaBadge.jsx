export default function QuotaBadge({ quota }) {
  if (!quota) return null
  const usagePct = Math.round((quota.used / quota.limit) * 100)
  return (
    <div className="quota-badge">
      <div>{quota.provider}</div>
      <div>API 사용량 {quota.used}/{quota.limit} ({usagePct}%)</div>
    </div>
  )
}
