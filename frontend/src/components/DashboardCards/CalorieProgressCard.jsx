export default function CalorieProgressCard({ summary }) {
  const { total_calories, calorie_goal, total_protein, total_carbohydrates, total_fat, total_fiber } = summary
  const pct = Math.min(Math.round((total_calories / calorie_goal) * 100), 100)

  const macros = [
    { label: 'Protein',   value: total_protein,       max: 150, color: 'bg-blue-500' },
    { label: 'Carbs',     value: total_carbohydrates,  max: 300, color: 'bg-yellow-400' },
    { label: 'Fat',       value: total_fat,            max: 80,  color: 'bg-red-400' },
    { label: 'Fiber',     value: total_fiber,          max: 35,  color: 'bg-green-500' },
  ]

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-semibold text-gray-900">Today's Nutrition</h3>
        <span className="text-sm text-gray-500">
          {Math.round(total_calories)} / {calorie_goal} kcal
        </span>
      </div>

      {/* Calorie bar */}
      <div className="mb-4">
        <div className="flex justify-between text-xs text-gray-500 mb-1">
          <span>Calories consumed</span>
          <span className={pct >= 100 ? 'text-red-500 font-medium' : 'text-primary-600 font-medium'}>{pct}%</span>
        </div>
        <div className="h-3 bg-gray-100 rounded-full overflow-hidden">
          <div
            className={`h-full rounded-full transition-all duration-500 ${pct >= 100 ? 'bg-red-400' : 'bg-primary-500'}`}
            style={{ width: `${pct}%` }}
          />
        </div>
      </div>

      {/* Macro bars */}
      <div className="grid grid-cols-2 gap-3">
        {macros.map(({ label, value, max, color }) => {
          const mpct = Math.min(Math.round((value / max) * 100), 100)
          return (
            <div key={label}>
              <div className="flex justify-between text-xs text-gray-500 mb-1">
                <span>{label}</span>
                <span>{Math.round(value)}g</span>
              </div>
              <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                <div className={`h-full rounded-full ${color}`} style={{ width: `${mpct}%` }} />
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
