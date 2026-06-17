export default function StatCard({ title, value, subtitle, icon, bg }) {
  return (
    <div className="card flex items-start gap-4">
      <div className={`${bg} p-3 rounded-xl flex-shrink-0`}>{icon}</div>
      <div className="min-w-0">
        <p className="text-xs text-gray-500 truncate">{title}</p>
        <p className="text-lg font-bold text-gray-900 truncate">{value}</p>
        {subtitle && <p className="text-xs text-gray-400 capitalize truncate">{subtitle}</p>}
      </div>
    </div>
  )
}
