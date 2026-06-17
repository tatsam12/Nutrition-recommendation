const FALLBACK_IMG = 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=60&q=80'

export default function RecentFoodsList({ logs }) {
  return (
    <div className="card">
      <h3 className="font-semibold text-gray-900 mb-4">Recently Consumed</h3>
      {logs.length === 0 ? (
        <p className="text-sm text-gray-400 text-center py-6">No food logged yet today</p>
      ) : (
        <div className="space-y-3">
          {logs.map(log => (
            <div key={log.id} className="flex items-center gap-3">
              <img
                src={log.food?.image_url || FALLBACK_IMG}
                alt={log.food?.food_name}
                onError={e => { e.target.src = FALLBACK_IMG }}
                className="w-10 h-10 rounded-lg object-cover flex-shrink-0"
              />
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-800 truncate">{log.food?.food_name}</p>
                <p className="text-xs text-gray-400 capitalize">{log.meal_type}</p>
              </div>
              <span className="text-xs font-semibold text-orange-500 flex-shrink-0">
                {Math.round(log.calories)} kcal
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
