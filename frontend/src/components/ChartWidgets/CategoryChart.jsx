import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

export default function CategoryChart({ data }) {
  return (
    <div className="card">
      <h3 className="font-semibold text-gray-900 mb-4">Food Category (7 days)</h3>
      {data.length === 0 ? (
        <p className="text-sm text-gray-400 text-center py-12">No data yet</p>
      ) : (
        <ResponsiveContainer width="100%" height={200}>
          <BarChart data={data} margin={{ top: 5, right: 10, left: -20, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
            <XAxis dataKey="category" tick={{ fontSize: 10, fill: '#94a3b8' }} interval={0}
              angle={-30} textAnchor="end" height={50} />
            <YAxis tick={{ fontSize: 11, fill: '#94a3b8' }} />
            <Tooltip formatter={(v) => [`${Math.round(v)} kcal`, 'Calories']} />
            <Bar dataKey="calories" fill="#22c55e" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      )}
    </div>
  )
}
