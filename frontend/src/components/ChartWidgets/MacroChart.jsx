import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts'

const COLORS = ['#3b82f6', '#f59e0b', '#ef4444', '#22c55e']

export default function MacroChart({ data }) {
  if (!data) return null

  const chartData = [
    { name: 'Protein',   value: Math.round(data.protein || 0) },
    { name: 'Carbs',     value: Math.round(data.carbohydrates || 0) },
    { name: 'Fat',       value: Math.round(data.fat || 0) },
    { name: 'Fiber',     value: Math.round(data.fiber || 0) },
  ].filter(d => d.value > 0)

  return (
    <div className="card">
      <h3 className="font-semibold text-gray-900 mb-4">Macronutrient Distribution</h3>
      {chartData.length === 0 ? (
        <p className="text-sm text-gray-400 text-center py-12">Log food to see macros</p>
      ) : (
        <ResponsiveContainer width="100%" height={200}>
          <PieChart>
            <Pie data={chartData} cx="50%" cy="50%" innerRadius={50} outerRadius={80}
              paddingAngle={3} dataKey="value">
              {chartData.map((_, i) => (
                <Cell key={i} fill={COLORS[i % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip formatter={(v, n) => [`${v}g`, n]} />
            <Legend wrapperStyle={{ fontSize: 11 }} />
          </PieChart>
        </ResponsiveContainer>
      )}
    </div>
  )
}
