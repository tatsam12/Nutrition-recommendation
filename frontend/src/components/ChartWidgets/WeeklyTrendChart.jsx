import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend,
} from 'recharts'

export default function WeeklyTrendChart({ data }) {
  return (
    <div className="card">
      <h3 className="font-semibold text-gray-900 mb-4">Weekly Calorie Trend</h3>
      <ResponsiveContainer width="100%" height={200}>
        <AreaChart data={data} margin={{ top: 5, right: 10, left: -20, bottom: 0 }}>
          <defs>
            <linearGradient id="calGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%"  stopColor="#22c55e" stopOpacity={0.3} />
              <stop offset="95%" stopColor="#22c55e" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
          <XAxis dataKey="day" tick={{ fontSize: 11, fill: '#94a3b8' }} />
          <YAxis tick={{ fontSize: 11, fill: '#94a3b8' }} />
          <Tooltip
            contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,.08)' }}
            formatter={(v) => [`${Math.round(v)} kcal`, 'Calories']}
          />
          <Area type="monotone" dataKey="calories" stroke="#22c55e" strokeWidth={2}
            fill="url(#calGrad)" dot={{ r: 3, fill: '#22c55e' }} />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  )
}
